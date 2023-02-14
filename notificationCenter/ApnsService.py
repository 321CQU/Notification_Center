from grpc.aio import ServicerContext
from grpc import StatusCode

from micro_services_protobuf.notification_center import apns_pb2
from micro_services_protobuf.notification_center import service_pb2_grpc as notification_grpc
from micro_services_protobuf.common_pb2 import DefaultResponse

from notificationCenter.models.apnsModels import AppleNotification
from utils.sqlManager import SqlManager
from .utils.appleAPNsHelper import AppleAPNsHelper


class ApnsService(notification_grpc.ApnsServicer):
    async def SetUserApns(self, request: apns_pb2.SetUserApnsRequest, context):
        async with SqlManager().cursor() as cursor:
            await cursor.execute('select count(uid) from Apns where uid = %s limit 1', (request.uid,))
            temp_result = await cursor.fetchone()
            if temp_result[0] == 1:
                await cursor.execute('update Apns set apn = %s where uid = %s', (request.apn, request.uid))
            else:
                await cursor.execute('insert into Apns (uid, apn) values (%s, %s)', (request.uid, request.apn))
        return DefaultResponse(msg='success')

    async def SendNotificationToUser(self, request: apns_pb2.SendApnsNotificationRequest, context: ServicerContext):
        async with SqlManager().cursor() as cursor:
            await cursor.execute('select apn from Apns where uid = %s', (request.uid,))
            apn = await cursor.fetchone()
            if apn is None:
                await context.abort(StatusCode.UNAVAILABLE, '无法查询到相关用户')
            apns_helper = AppleAPNsHelper()
            await apns_helper.send_message(apn[0], AppleNotification.from_proto(request.notification).launch_request())
        return DefaultResponse(msg='success')
