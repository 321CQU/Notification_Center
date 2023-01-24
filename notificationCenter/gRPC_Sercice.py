from notificationCenter.models.apnsModels import AppleNotification
from utils.sqlManager import SqlManager
from notificationCenter.proto import apns_pb2, apns_pb2_grpc
from .utils.appleAPNsHelper import AppleAPNsHelper


class ApnsService(apns_pb2_grpc.ApnsServicer):
    async def SetUserApns(self, request: apns_pb2.SetUserApnsRequest, context):
        async with SqlManager().cursor() as cursor:
            await cursor.execute('select * from UserApns where Sid = %s', (request.sid,))
            temp_result = await cursor.fetchall()
            if len(temp_result) == 1:
                await cursor.execute('update UserApns set Apn = %s where Sid = %s', (request.apn, request.sid))
            elif len(temp_result) == 0:
                await cursor.execute('insert into UserApns (Sid, Apn) values (%s, %s)', (request.sid, request.apn))
        return apns_pb2.DefaultResponse(status=1, msg='success')

    async def SendNotificationToUser(self, request: apns_pb2.SendNotificationRequest, context):
        async with SqlManager().cursor() as cursor:
            await cursor.execute('select Apn from UserApns where Sid = %s', (request.sid,))
            apn = await cursor.fetchone()
            if len(apn) == 0:
                return apns_pb2.DefaultResponse(status=0, msg="Can't find related user")
            apns_helper = AppleAPNsHelper()
            await apns_helper.send_message(apn[0], AppleNotification.from_proto(request.notification).launch_request())
        return apns_pb2.DefaultResponse(status=1, msg='success')

