import asyncio
import logging
import grpc

from utils.tools.configManager import ConfigReader
from notificationCenter.gRPC_Sercice import ApnsService

from micro_services_protobuf.notification_center import apns_pb2_grpc


async def serve():
    reader = ConfigReader()
    port = reader.get_config('gRPCServiceConfig', 'ApnServicePort')

    server = grpc.aio.server()
    apns_pb2_grpc.add_ApnsServicer_to_server(
        ApnsService(), server)
    server.add_insecure_port('[::]:' + port)
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.new_event_loop().run_until_complete(serve())
