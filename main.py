import asyncio
import logging
import grpc

from utils.sqlManager import SqlManager
from notificationCenter.proto import apns_pb2, apns_pb2_grpc


class ApnsService(apns_pb2_grpc.ApnsServicer):
    async def SetUserApns(self, request: apns_pb2.SetUserApnsRequest, context):
        sql_manager = SqlManager()
        sql_manager.execute('select * from UserApns where Sid = ?', (request.sid,))
        temp_result = sql_manager.fetchall()
        if len(temp_result) == 1:
            sql_manager.execute('update UserApns set Apn = ? where Sid = ?', (request.apn, request.sid))
        elif len(temp_result) == 0:
            sql_manager.execute('insert into UserApns (Sid, Apn) values (?, ?)', (request.sid, request.apn))
        return apns_pb2.SetUserApnsResponse(status=1, msg='success')


async def serve():
    server = grpc.aio.server()
    apns_pb2_grpc.add_ApnsServicer_to_server(
        ApnsService(), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(serve())
