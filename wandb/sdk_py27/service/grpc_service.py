#!/usr/bin/env python
"""WIP wandb grpc server."""

from concurrent import futures
import datetime
import logging
import multiprocessing
import os
import sys
import tempfile
import time

import grpc  # type: ignore
import setproctitle  # type: ignore
from six.moves import queue
import wandb
from wandb.proto import wandb_internal_pb2 as pb
from wandb.proto import wandb_server_pb2
from wandb.proto import wandb_server_pb2_grpc
from wandb.proto import wandb_telemetry_pb2 as tpb

from .. import lib as wandb_lib
from ..interface import interface

if wandb.TYPE_CHECKING:
    from typing import TYPE_CHECKING
    from typing import Any, Dict, Optional

    if TYPE_CHECKING:

        class GrpcServerType(object):
            def __init__(self):
                pass

            def stop(self, num):
                pass


class InternalServiceServicer(wandb_server_pb2_grpc.InternalServiceServicer):
    """Provides methods that implement functionality of route guide server."""

    # _server: "GrpcServerType"
    # _backend: "GrpcBackend"

    def __init__(self, server, backend):
        self._server = server
        self._backend = backend

    def RunUpdate(  # noqa: N802
        self, run_data, context
    ):
        if not run_data.run_id:
            run_data.run_id = wandb_lib.runid.generate_id()
        # Record telemetry info about grpc server
        run_data.telemetry.feature.grpc = True
        run_data.telemetry.cli_version = wandb.__version__
        assert self._backend and self._backend._interface
        result = self._backend._interface._communicate_run(run_data)
        assert result  # TODO: handle errors
        return result

    def RunStart(  # noqa: N802
        self, run_start, context
    ):
        # initiate run (stats and metadata probing)
        assert self._backend and self._backend._interface
        result = self._backend._interface._communicate_run_start(run_start)
        assert result  # TODO: handle errors
        return result

    def CheckVersion(  # noqa: N802
        self, check_version, context
    ):
        assert self._backend and self._backend._interface
        result = self._backend._interface._communicate_check_version(check_version)
        assert result  # TODO: handle errors
        return result

    def PollExit(  # noqa: N802
        self, poll_exit, context
    ):
        assert self._backend and self._backend._interface
        result = self._backend._interface.communicate_poll_exit()
        assert result  # TODO: handle errors
        return result

    def GetSummary(  # noqa: N802
        self, get_summary, context
    ):
        assert self._backend and self._backend._interface
        result = self._backend._interface.communicate_summary()
        assert result  # TODO: handle errors
        return result

    def SampledHistory(  # noqa: N802
        self, sampled_history, context
    ):
        assert self._backend and self._backend._interface
        result = self._backend._interface.communicate_sampled_history()
        assert result  # TODO: handle errors
        return result

    def Shutdown(  # noqa: N802
        self, shutdown, context
    ):
        assert self._backend and self._backend._interface
        self._backend._interface._communicate_shutdown()
        result = pb.ShutdownResponse()
        return result

    def RunExit(  # noqa: N802
        self, exit_data, context
    ):
        assert self._backend and self._backend._interface
        self._backend._interface.publish_exit(exit_data.exit_code)
        result = pb.RunExitResult()
        return result

    def Log(  # noqa: N802
        self, history, context
    ):
        assert self._backend and self._backend._interface
        self._backend._interface._publish_history(history)
        # make up a response even though this was async
        result = pb.HistoryResult()
        return result

    def Summary(  # noqa: N802
        self, summary, context
    ):
        assert self._backend and self._backend._interface
        self._backend._interface._publish_summary(summary)
        # make up a response even though this was async
        result = pb.SummaryResult()
        return result

    def Telemetry(  # noqa: N802
        self, telem, context
    ):
        assert self._backend and self._backend._interface
        self._backend._interface._publish_telemetry(telem)
        # make up a response even though this was async
        result = tpb.TelemetryResult()
        return result

    def Output(  # noqa: N802
        self, output_data, context
    ):
        assert self._backend and self._backend._interface
        self._backend._interface._publish_output(output_data)
        # make up a response even though this was async
        result = pb.OutputResult()
        return result

    def Config(  # noqa: N802
        self, config_data, context
    ):
        assert self._backend and self._backend._interface
        self._backend._interface._publish_config(config_data)
        # make up a response even though this was async
        result = pb.ConfigResult()
        return result

    def Metric(  # noqa: N802
        self, metric, context
    ):
        assert self._backend and self._backend._interface
        self._backend._interface._publish_metric(metric)
        # make up a response even though this was async
        result = pb.MetricResult()
        return result

    def ServerShutdown(  # noqa: N802
        self,
        request,
        context,
    ):
        assert self._backend and self._backend._interface
        self._backend.cleanup()
        result = wandb_server_pb2.ServerShutdownResponse()
        self._server.stop(5)
        return result

    def ServerStatus(  # noqa: N802
        self,
        request,
        context,
    ):
        assert self._backend and self._backend._interface
        result = wandb_server_pb2.ServerStatusResponse()
        return result


# TODO(jhr): this should be merged with code in backend/backend.py ensure launched
class GrpcBackend:
    # _interface: interface.BackendSender
    # _settings: Dict[str, Any]
    # _process: multiprocessing.process.BaseProcess
    # _record_q: "queue.Queue[pb.Record]"
    # _result_q: "queue.Queue[pb.Result]"
    # _monitor_pid: Optional[int]

    def __init__(self, pid = None, debug = False):
        self._done = False
        self._record_q = multiprocessing.Queue()
        self._result_q = multiprocessing.Queue()
        self._process = multiprocessing.current_process()
        self._settings = self._make_settings()
        self._monitor_pid = pid
        self._debug = debug

        if debug:
            self._settings["log_internal"] = None

        self._interface = wandb.wandb_sdk.interface.interface.BackendSender(
            record_q=self._record_q,
            result_q=self._result_q,
            process=self._process,
            process_check=False,
        )

    def _make_settings(self):
        log_level = logging.DEBUG
        start_time = time.time()
        start_datetime = datetime.datetime.now()
        timespec = datetime.datetime.strftime(start_datetime, "%Y%m%d_%H%M%S")

        wandb_dir = "wandb"
        pid = os.getpid()
        run_path = "run-{}-{}-server".format(timespec, pid)
        run_dir = os.path.join(wandb_dir, run_path)
        files_dir = os.path.join(run_dir, "files")
        sync_file = os.path.join(run_dir, "run-{}.wandb".format(start_time))
        os.makedirs(files_dir)
        settings = dict(
            log_internal=os.path.join(run_dir, "internal.log"),
            files_dir=files_dir,
            _start_time=start_time,
            _start_datetime=start_datetime,
            disable_code=None,
            code_program=None,
            save_code=None,
            sync_file=sync_file,
            _internal_queue_timeout=20,
            _internal_check_process=8,
            _disable_meta=True,
            _disable_stats=False,
            git_remote=None,
            program=None,
            resume=None,
            ignore_globs=(),
            offline=None,
            _log_level=log_level,
            run_id=None,
            entity=None,
            project=None,
            run_group=None,
            run_job_type=None,
            run_tags=None,
            run_name=None,
            run_notes=None,
            _jupyter=None,
            _kaggle=None,
            _offline=None,
            email=None,
            silent=None,
        )
        return settings

    def run(self, port):
        try:
            wandb.wandb_sdk.internal.internal.wandb_internal(
                settings=self._settings,
                record_q=self._record_q,
                result_q=self._result_q,
                port=port,
                user_pid=self._monitor_pid,
            )
        except KeyboardInterrupt:
            pass

    def cleanup(self):
        # TODO: make _done atomic
        if self._done:
            return
        self._done = True
        self._interface.join()


def serve(
    backend, port, port_filename = None, address = None
):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    try:
        wandb_server_pb2_grpc.add_InternalServiceServicer_to_server(
            InternalServiceServicer(server, backend), server
        )
        port = server.add_insecure_port("localhost:{}".format(port))
        server.start()

        if port_filename:
            dname, bname = os.path.split(port_filename)
            f = tempfile.NamedTemporaryFile(
                prefix=bname, dir=dname, mode="w", delete=False
            )
            tmp_filename = f.name
            try:
                with f:
                    f.write("%d" % port)
                os.rename(tmp_filename, port_filename)
            except Exception:
                os.unlink(tmp_filename)
                raise

        # server.wait_for_termination()
    except KeyboardInterrupt:
        backend.cleanup()
        server.stop(0)
        raise
    except Exception:
        backend.cleanup()
        server.stop(0)
        raise
    return port


def main(
    port = None,
    port_filename = None,
    address = None,
    pid = None,
    run = None,
    rundir = None,
    debug = False,
):
    if debug:
        logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

    backend = GrpcBackend(pid=pid, debug=debug)
    port = serve(backend, port or 0, port_filename=port_filename, address=address)
    setproctitle.setproctitle("wandb_internal[grpc:{}]".format(port))
    backend.run(port=port)
    backend.cleanup()


if __name__ == "__main__":
    main()
