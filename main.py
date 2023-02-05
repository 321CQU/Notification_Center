import asyncio
import logging
import grpc

from notificationCenter.gRPC_Sercice import ApnsService

from micro_services_protobuf.notification_center import apns_pb2_grpc
from _321CQU.tools.gRPCManager import gRPCManager, ServiceEnum


async def serve():
    port = gRPCManager().get_service_config(ServiceEnum.NotificationCenter)[1]

    server = grpc.aio.server()
    apns_pb2_grpc.add_ApnsServicer_to_server(
        ApnsService(), server)
    server.add_insecure_port('[::]:' + port)
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    print("启动 NotificationCenter服务")
    logging.basicConfig(level=logging.INFO)
    asyncio.new_event_loop().run_until_complete(serve())
