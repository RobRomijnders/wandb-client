import base64
import json
import os
import tarfile
import tempfile
import time
from typing import Any, Dict, Optional

from google.cloud import storage  # type: ignore
import kubernetes
from kubernetes import client  # type: ignore
import wandb
from wandb.errors import LaunchError
from wandb.sdk.launch.builder.abstract import AbstractBuilder
from wandb.util import get_module

from .build import _create_build_ctx, generate_dockerfile
from .._project_spec import (
    create_metadata_file,
    EntryPoint,
    get_entry_point_command,
    LaunchProject,
)
from ..utils import get_kube_context_and_api_client, sanitize_wandb_api_key


_DEFAULT_BUILD_TIMEOUT_SECS = 1800  # 30 minute build timeout


def _create_dockerfile_configmap(
    config_map_name: str, context_path: str
) -> client.V1ConfigMap:
    with open(os.path.join(context_path, "Dockerfile.wandb-autogenerated"), "rb") as f:
        docker_file_bytes = f.read()

    build_config_map = client.V1ConfigMap(
        metadata=client.V1ObjectMeta(
            name=config_map_name, namespace="wandb", labels={"wandb": "launch"}
        ),
        binary_data={
            "Dockerfile": base64.b64encode(docker_file_bytes).decode("UTF-8"),
        },
        immutable=True,
    )
    return build_config_map


def _wait_for_completion(
    batch_client: client.BatchV1Api, job_name: str, deadline_secs: Optional[int] = None
) -> bool:
    start_time = time.time()
    while True:
        job = batch_client.read_namespaced_job_status(job_name, "wandb")
        if job.status.succeeded is not None and job.status.succeeded >= 1:
            return True
        elif job.status.failed is not None and job.status.failed >= 1:
            return False
        wandb.termlog("Waiting for build job to complete...")
        if deadline_secs is not None and time.time() - start_time > deadline_secs:
            return False

        time.sleep(5)


class KanikoBuilder(AbstractBuilder):
    type = "kaniko"

    def __init__(self, builder_config: Dict[str, Any]):
        super().__init__(builder_config)
        self.config_map_name = builder_config.get(
            "config-map-name", "wandb-launch-build-context"
        )
        self.build_job_name = builder_config.get(
            "build-job-name", "wandb-launch-container-build"
        )
        self.cloud_provider = builder_config.get("cloud-provider", None)
        if self.cloud_provider is None:
            raise LaunchError("Kaniko builder requires cloud-provider info")
        if not builder_config.get("credentials"):
            # if no cloud provider info given, assume running in instance mode
            # kaniko pod will have access to build context store and ecr
            wandb.termlog("Kaniko builder running in instance mode")

        self.build_context_store = builder_config.get("build-context-store", None)
        if self.build_context_store is None:
            raise LaunchError("build-context-store is not set in cloud-provider")
        credentials_config = builder_config.get("credentials", {})
        self.credentials_secret_name = credentials_config.get("secret-name")
        self.credentials_secret_mount_path = credentials_config.get("secret-mount-path")
        if bool(self.credentials_secret_name) != bool(
            self.credentials_secret_mount_path
        ):
            raise LaunchError(
                "Must provide secret-name and secret-mount-path or neither"
            )

    def _create_docker_ecr_config_map(self, corev1_client: client.CoreV1Api) -> None:
        corev1_client.V1VolumeMount(name="docker-config", mount_path="/kaniko/.docker/")
        if self.cloud_provider == "AWS":
            ecr_config_map = corev1_client.V1ConfigMap(
                api_version="v1",
                kind="ConfigMap",
                metadata=corev1_client.V1ObjectMeta(
                    name="docker-config",
                    namespace="wandb",
                ),
                data={"config.json": json.dumps({"credsStore": "ecr-login"})},
            )
            corev1_client.create_namespaced_config_map("wandb", ecr_config_map)

    def _delete_docker_ecr_config_map(self, client: client.CoreV1Api) -> None:
        client.delete_namespaced_config_map("docker-config", "wandb")

    def _upload_build_context(self, run_id: str, context_path: str) -> str:
        # creat a tar archive of the build context and upload it to s3
        context_file = tempfile.NamedTemporaryFile(delete=False)
        with tarfile.TarFile.open(fileobj=context_file, mode="w:gz") as context_tgz:
            context_tgz.add(context_path, arcname=".")

        if self.builder_config.get("cloud-provider") == "AWS":
            boto3 = get_module("boto3", "aws requires boto3")
            botocore = get_module("botocore", "aws requires botocore")

            s3_client = boto3.client("s3")
            try:
                s3_client.upload_file(
                    context_tgz.name,
                    self.build_context_store,
                    f"{run_id}.tgz",
                )
            except botocore.exceptions.ClientError as e:
                raise LaunchError(f"Failed to upload build context to S3: {e}")

            return f"s3://{self.build_context_store}/{run_id}.tgz"
        # TODO: support gcp and azur cloud providers
        elif self.builder_config.get("cloud-provider") == "gcp":
            storage_client = storage.Client()
            try:
                bucket = storage_client.bucket(self.build_context_store)
                blob = bucket.blob(f"{run_id}.tgz")
                blob.upload_from_filename(context_tgz.name)
            except Exception as e:
                raise LaunchError(f"Failed to upload build context to GCP: {e}")
            return f"gs://{self.build_context_store}/{run_id}.tgz"
        else:
            raise LaunchError("Unsupported storage provider")

    def build_image(
        self,
        launch_project: LaunchProject,
        repository: Optional[str],
        entrypoint: Optional[EntryPoint],
        docker_args: Dict[str, Any],
    ) -> str:
        if repository is None:
            raise LaunchError("repository is required for kaniko builder")
        image_uri = f"{repository}:{launch_project.run_id}"
        entry_cmd = get_entry_point_command(entrypoint, launch_project.override_args)

        # kaniko builder doesn't seem to work with a custom user id, need more investigation
        dockerfile_str = generate_dockerfile(
            launch_project, entry_cmd, launch_project.resource, self.type
        )
        create_metadata_file(
            launch_project,
            image_uri,
            sanitize_wandb_api_key(entry_cmd),
            docker_args,
            sanitize_wandb_api_key(dockerfile_str),
        )
        context_path = _create_build_ctx(launch_project, dockerfile_str)
        run_id = launch_project.run_id

        api_client = get_kube_context_and_api_client(
            kubernetes, launch_project.resource_args
        )
        build_job_name = f"{self.build_job_name}-{run_id}"
        config_map_name = f"{self.config_map_name}-{run_id}"

        build_context = self._upload_build_context(run_id, context_path)
        dockerfile_config_map = _create_dockerfile_configmap(
            self.config_map_name, context_path
        )
        build_job = self._create_kaniko_job(
            build_job_name,
            dockerfile_config_map.metadata.name,
            repository,
            image_uri,
            build_context,
        )
        # TODO: use same client as kuberentes.py
        batch_v1 = client.BatchV1Api(api_client)
        core_v1 = client.CoreV1Api(api_client)

        try:
            core_v1.create_namespaced_config_map("wandb", dockerfile_config_map)
            self._create_docker_ecr_config_map(core_v1)
            batch_v1.create_namespaced_job("wandb", build_job)

            # wait for double the job deadline since it might take time to schedule
            if not _wait_for_completion(
                batch_v1, build_job_name, 2 * _DEFAULT_BUILD_TIMEOUT_SECS
            ):
                raise Exception(f"Failed to build image in kaniko for job {run_id}")
        except client.ApiException as e:
            wandb.termerror(f"Exception when creating Kubernetes resources: {e}\n")
        finally:
            wandb.termlog("cleaning up resources")
            try:
                # should we clean up the s3 build contexts? can set bucket level policy to auto deletion
                batch_v1.delete_namespaced_job(build_job_name, "wandb")
                core_v1.delete_namespaced_config_map(config_map_name, "wandb")
                self._delete_docker_ecr_config_map(core_v1)
            except Exception as e:
                wandb.termerror(f"Exception during Kubernetes resource clean up {e}")

        return image_uri

    def _create_kaniko_job(
        self,
        job_name: str,
        config_map_name: str,
        repository: str,
        image_tag: str,
        build_context_path: str,
    ) -> client.V1Job:

        volume_mounts = [
            client.V1VolumeMount(
                name="build-context-config-map", mount_path="/etc/config"
            )
        ]
        volumes = [
            client.V1Volume(
                name="build-context-config-map",
                config_map=client.V1ConfigMapVolumeSource(
                    name=config_map_name,
                ),
            ),
        ]
        if (
            self.credentials_secret_name is not None
            and self.credentials_secret_mount_path is not None
        ):
            volume_mounts += [
                client.V1VolumeMount(
                    name=self.credentials_secret_name,
                    mount_path=self.credentials_secret_mount_path,
                    read_only=True,
                ),
                client.V1VolumeMount(
                    name="docker-config", mount_path="/kaniko/.docker/"
                ),
            ]
            volumes += [
                client.V1Volume(
                    name="docker-config",
                    config_map=client.V1ConfigMapVolumeSource(
                        name="docker-config",
                    ),
                ),
                client.V1Volume(
                    name=self.credentials_secret_name,
                    secret=client.V1SecretVolumeSource(
                        secret_name=self.credentials_secret_name
                    ),
                ),
            ]
        # Configurate Pod template container
        container = client.V1Container(
            name="wandb-container-build",
            image="gcr.io/kaniko-project/executor:debug",
            args=[
                f"--context={build_context_path}",
                "--dockerfile=/etc/config/Dockerfile",
                f"--destination={image_tag}",
                "--cache=true",
                f"--cache-repo={repository}",
            ],
            volume_mounts=volume_mounts,
        )
        # Create and configure a spec section
        template = client.V1PodTemplateSpec(
            metadata=client.V1ObjectMeta(labels={"wandb": "launch"}),
            spec=client.V1PodSpec(
                restart_policy="Never",
                active_deadline_seconds=_DEFAULT_BUILD_TIMEOUT_SECS,
                containers=[container],
                volumes=volumes,
            ),
        )
        # Create the specification of job
        spec = client.V1JobSpec(template=template, backoff_limit=1)
        job = client.V1Job(
            api_version="batch/v1",
            kind="Job",
            metadata=client.V1ObjectMeta(
                name=job_name, namespace="wandb", labels={"wandb": "launch"}
            ),
            spec=spec,
        )

        return job
