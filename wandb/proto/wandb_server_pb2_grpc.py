# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
import grpc

from wandb.proto import wandb_internal_pb2 as wandb_dot_proto_dot_wandb__internal__pb2
from wandb.proto import wandb_server_pb2 as wandb_dot_proto_dot_wandb__server__pb2
from wandb.proto import wandb_telemetry_pb2 as wandb_dot_proto_dot_wandb__telemetry__pb2


class InternalServiceStub(object):
  # missing associated documentation comment in .proto file
  pass

  def __init__(self, channel):
    """Constructor.

    Args:
      channel: A grpc.Channel.
    """
    self.RunUpdate = channel.unary_unary(
        '/wandb_internal.InternalService/RunUpdate',
        request_serializer=wandb_dot_proto_dot_wandb__internal__pb2.RunRecord.SerializeToString,
        response_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.RunUpdateResult.FromString,
        )
    self.RunStart = channel.unary_unary(
        '/wandb_internal.InternalService/RunStart',
        request_serializer=wandb_dot_proto_dot_wandb__internal__pb2.RunStartRequest.SerializeToString,
        response_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.RunStartResponse.FromString,
        )
    self.GetSummary = channel.unary_unary(
        '/wandb_internal.InternalService/GetSummary',
        request_serializer=wandb_dot_proto_dot_wandb__internal__pb2.GetSummaryRequest.SerializeToString,
        response_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.GetSummaryResponse.FromString,
        )
    self.SampledHistory = channel.unary_unary(
        '/wandb_internal.InternalService/SampledHistory',
        request_serializer=wandb_dot_proto_dot_wandb__internal__pb2.SampledHistoryRequest.SerializeToString,
        response_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.SampledHistoryResponse.FromString,
        )
    self.PollExit = channel.unary_unary(
        '/wandb_internal.InternalService/PollExit',
        request_serializer=wandb_dot_proto_dot_wandb__internal__pb2.PollExitRequest.SerializeToString,
        response_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.PollExitResponse.FromString,
        )
    self.Shutdown = channel.unary_unary(
        '/wandb_internal.InternalService/Shutdown',
        request_serializer=wandb_dot_proto_dot_wandb__internal__pb2.ShutdownRequest.SerializeToString,
        response_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.ShutdownResponse.FromString,
        )
    self.RunExit = channel.unary_unary(
        '/wandb_internal.InternalService/RunExit',
        request_serializer=wandb_dot_proto_dot_wandb__internal__pb2.RunExitRecord.SerializeToString,
        response_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.RunExitResult.FromString,
        )
    self.Metric = channel.unary_unary(
        '/wandb_internal.InternalService/Metric',
        request_serializer=wandb_dot_proto_dot_wandb__internal__pb2.MetricRecord.SerializeToString,
        response_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.MetricResult.FromString,
        )
    self.Log = channel.unary_unary(
        '/wandb_internal.InternalService/Log',
        request_serializer=wandb_dot_proto_dot_wandb__internal__pb2.HistoryRecord.SerializeToString,
        response_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.HistoryResult.FromString,
        )
    self.Summary = channel.unary_unary(
        '/wandb_internal.InternalService/Summary',
        request_serializer=wandb_dot_proto_dot_wandb__internal__pb2.SummaryRecord.SerializeToString,
        response_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.SummaryResult.FromString,
        )
    self.Config = channel.unary_unary(
        '/wandb_internal.InternalService/Config',
        request_serializer=wandb_dot_proto_dot_wandb__internal__pb2.ConfigRecord.SerializeToString,
        response_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.ConfigResult.FromString,
        )
    self.Output = channel.unary_unary(
        '/wandb_internal.InternalService/Output',
        request_serializer=wandb_dot_proto_dot_wandb__internal__pb2.OutputRecord.SerializeToString,
        response_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.OutputResult.FromString,
        )
    self.Telemetry = channel.unary_unary(
        '/wandb_internal.InternalService/Telemetry',
        request_serializer=wandb_dot_proto_dot_wandb__telemetry__pb2.TelemetryRecord.SerializeToString,
        response_deserializer=wandb_dot_proto_dot_wandb__telemetry__pb2.TelemetryResult.FromString,
        )
    self.CheckVersion = channel.unary_unary(
        '/wandb_internal.InternalService/CheckVersion',
        request_serializer=wandb_dot_proto_dot_wandb__internal__pb2.CheckVersionRequest.SerializeToString,
        response_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.CheckVersionResponse.FromString,
        )
    self.ServerShutdown = channel.unary_unary(
        '/wandb_internal.InternalService/ServerShutdown',
        request_serializer=wandb_dot_proto_dot_wandb__server__pb2.ServerShutdownRequest.SerializeToString,
        response_deserializer=wandb_dot_proto_dot_wandb__server__pb2.ServerShutdownResponse.FromString,
        )
    self.ServerStatus = channel.unary_unary(
        '/wandb_internal.InternalService/ServerStatus',
        request_serializer=wandb_dot_proto_dot_wandb__server__pb2.ServerStatusRequest.SerializeToString,
        response_deserializer=wandb_dot_proto_dot_wandb__server__pb2.ServerStatusResponse.FromString,
        )


class InternalServiceServicer(object):
  # missing associated documentation comment in .proto file
  pass

  def RunUpdate(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def RunStart(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def GetSummary(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def SampledHistory(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def PollExit(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Shutdown(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def RunExit(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Metric(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Log(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Summary(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Config(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Output(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def Telemetry(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def CheckVersion(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ServerShutdown(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')

  def ServerStatus(self, request, context):
    # missing associated documentation comment in .proto file
    pass
    context.set_code(grpc.StatusCode.UNIMPLEMENTED)
    context.set_details('Method not implemented!')
    raise NotImplementedError('Method not implemented!')


def add_InternalServiceServicer_to_server(servicer, server):
  rpc_method_handlers = {
      'RunUpdate': grpc.unary_unary_rpc_method_handler(
          servicer.RunUpdate,
          request_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.RunRecord.FromString,
          response_serializer=wandb_dot_proto_dot_wandb__internal__pb2.RunUpdateResult.SerializeToString,
      ),
      'RunStart': grpc.unary_unary_rpc_method_handler(
          servicer.RunStart,
          request_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.RunStartRequest.FromString,
          response_serializer=wandb_dot_proto_dot_wandb__internal__pb2.RunStartResponse.SerializeToString,
      ),
      'GetSummary': grpc.unary_unary_rpc_method_handler(
          servicer.GetSummary,
          request_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.GetSummaryRequest.FromString,
          response_serializer=wandb_dot_proto_dot_wandb__internal__pb2.GetSummaryResponse.SerializeToString,
      ),
      'SampledHistory': grpc.unary_unary_rpc_method_handler(
          servicer.SampledHistory,
          request_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.SampledHistoryRequest.FromString,
          response_serializer=wandb_dot_proto_dot_wandb__internal__pb2.SampledHistoryResponse.SerializeToString,
      ),
      'PollExit': grpc.unary_unary_rpc_method_handler(
          servicer.PollExit,
          request_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.PollExitRequest.FromString,
          response_serializer=wandb_dot_proto_dot_wandb__internal__pb2.PollExitResponse.SerializeToString,
      ),
      'Shutdown': grpc.unary_unary_rpc_method_handler(
          servicer.Shutdown,
          request_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.ShutdownRequest.FromString,
          response_serializer=wandb_dot_proto_dot_wandb__internal__pb2.ShutdownResponse.SerializeToString,
      ),
      'RunExit': grpc.unary_unary_rpc_method_handler(
          servicer.RunExit,
          request_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.RunExitRecord.FromString,
          response_serializer=wandb_dot_proto_dot_wandb__internal__pb2.RunExitResult.SerializeToString,
      ),
      'Metric': grpc.unary_unary_rpc_method_handler(
          servicer.Metric,
          request_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.MetricRecord.FromString,
          response_serializer=wandb_dot_proto_dot_wandb__internal__pb2.MetricResult.SerializeToString,
      ),
      'Log': grpc.unary_unary_rpc_method_handler(
          servicer.Log,
          request_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.HistoryRecord.FromString,
          response_serializer=wandb_dot_proto_dot_wandb__internal__pb2.HistoryResult.SerializeToString,
      ),
      'Summary': grpc.unary_unary_rpc_method_handler(
          servicer.Summary,
          request_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.SummaryRecord.FromString,
          response_serializer=wandb_dot_proto_dot_wandb__internal__pb2.SummaryResult.SerializeToString,
      ),
      'Config': grpc.unary_unary_rpc_method_handler(
          servicer.Config,
          request_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.ConfigRecord.FromString,
          response_serializer=wandb_dot_proto_dot_wandb__internal__pb2.ConfigResult.SerializeToString,
      ),
      'Output': grpc.unary_unary_rpc_method_handler(
          servicer.Output,
          request_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.OutputRecord.FromString,
          response_serializer=wandb_dot_proto_dot_wandb__internal__pb2.OutputResult.SerializeToString,
      ),
      'Telemetry': grpc.unary_unary_rpc_method_handler(
          servicer.Telemetry,
          request_deserializer=wandb_dot_proto_dot_wandb__telemetry__pb2.TelemetryRecord.FromString,
          response_serializer=wandb_dot_proto_dot_wandb__telemetry__pb2.TelemetryResult.SerializeToString,
      ),
      'CheckVersion': grpc.unary_unary_rpc_method_handler(
          servicer.CheckVersion,
          request_deserializer=wandb_dot_proto_dot_wandb__internal__pb2.CheckVersionRequest.FromString,
          response_serializer=wandb_dot_proto_dot_wandb__internal__pb2.CheckVersionResponse.SerializeToString,
      ),
      'ServerShutdown': grpc.unary_unary_rpc_method_handler(
          servicer.ServerShutdown,
          request_deserializer=wandb_dot_proto_dot_wandb__server__pb2.ServerShutdownRequest.FromString,
          response_serializer=wandb_dot_proto_dot_wandb__server__pb2.ServerShutdownResponse.SerializeToString,
      ),
      'ServerStatus': grpc.unary_unary_rpc_method_handler(
          servicer.ServerStatus,
          request_deserializer=wandb_dot_proto_dot_wandb__server__pb2.ServerStatusRequest.FromString,
          response_serializer=wandb_dot_proto_dot_wandb__server__pb2.ServerStatusResponse.SerializeToString,
      ),
  }
  generic_handler = grpc.method_handlers_generic_handler(
      'wandb_internal.InternalService', rpc_method_handlers)
  server.add_generic_rpc_handlers((generic_handler,))
