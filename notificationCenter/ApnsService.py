from grpc.aio import ServicerContext
from grpc import StatusCode

from micro_services_protobuf.notification_center import apns_pb2
from micro_services_protobuf.notification_center import service_pb2_grpc as notification_grpc
from micro_services_protobuf.common_pb2 import DefaultResponse

from _321CQU.sql_helper.SqlManager import DatabaseConfig

from notificationCenter.models.apnsModels import AppleNotification
from utils.sqlManager import NCSqlManager
from .utils.appleAPNsHelper import AppleAPNsHelper


class ApnsService(notification_grpc.ApnsServicer):
    async def SetUserApns(self, request: apns_pb2.SetUserApnsRequest, context):
        async with NCSqlManager().cursor(DatabaseConfig.Notification) as cursor:
            await cursor.execute('insert into Apns (uid, apn) values (%s, %s) on duplicate key update '
                                 'Apns.apn = apn', (request.uid, request.apn))
        return DefaultResponse(msg='success')

    async def SendNotificationToUser(self, request: apns_pb2.SendApnsNotificationRequest, context: ServicerContext):
        apns_helper = AppleAPNsHelper()
        await apns_helper.send_message(request.apn.hex(),
                                       AppleNotification.from_proto(request.notification).launch_request())
        return DefaultResponse(msg='success')
