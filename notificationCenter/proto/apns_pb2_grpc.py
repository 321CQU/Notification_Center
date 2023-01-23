# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from . import apns_pb2 as apns__pb2


class ApnsStub(object):
    """Missing associated documentation comment in .proto file."""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SetUserApns = channel.unary_unary(
                '/Apns/SetUserApns',
                request_serializer=apns__pb2.SetUserApnsRequest.SerializeToString,
                response_deserializer=apns__pb2.DefaultResponse.FromString,
                )
        self.SendNotificationToUser = channel.unary_unary(
                '/Apns/SendNotificationToUser',
                request_serializer=apns__pb2.SendNotificationRequest.SerializeToString,
                response_deserializer=apns__pb2.DefaultResponse.FromString,
                )


class ApnsServicer(object):
    """Missing associated documentation comment in .proto file."""

    def SetUserApns(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def SendNotificationToUser(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_ApnsServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SetUserApns': grpc.unary_unary_rpc_method_handler(
                    servicer.SetUserApns,
                    request_deserializer=apns__pb2.SetUserApnsRequest.FromString,
                    response_serializer=apns__pb2.DefaultResponse.SerializeToString,
            ),
            'SendNotificationToUser': grpc.unary_unary_rpc_method_handler(
                    servicer.SendNotificationToUser,
                    request_deserializer=apns__pb2.SendNotificationRequest.FromString,
                    response_serializer=apns__pb2.DefaultResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'Apns', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))


 # This class is part of an EXPERIMENTAL API.
class Apns(object):
    """Missing associated documentation comment in .proto file."""

    @staticmethod
    def SetUserApns(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Apns/SetUserApns',
            apns__pb2.SetUserApnsRequest.SerializeToString,
            apns__pb2.DefaultResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)

    @staticmethod
    def SendNotificationToUser(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(request, target, '/Apns/SendNotificationToUser',
            apns__pb2.SendNotificationRequest.SerializeToString,
            apns__pb2.DefaultResponse.FromString,
            options, channel_credentials,
            insecure, call_credentials, compression, wait_for_ready, timeout, metadata)
