from grpc import StatusCode
from grpc.aio import ServicerContext

from micro_services_protobuf.notification_center import service_pb2_grpc as notification_grpc
from micro_services_protobuf.notification_center import event_pb2 as notification_model
from micro_services_protobuf import common_pb2 as common_model
from micro_services_protobuf.protobuf_enum.notification_center import NotificationEvent

from _321CQU.sql_helper.SqlManager import DatabaseConfig

from notificationCenter.subscribe import handle_subscribe_update
from utils.sqlManager import NCSqlManager


__all__ = ['NotificationService']


async def _handle_update_score_query(request: notification_model.UpdateEventSubscribeRequest, context: ServicerContext):
    async with NCSqlManager().cursor(DatabaseConfig.User) as cursor:
        auth = request.extra_data.auth
        password = request.extra_data.password
        if auth == '' or password == '':
            await context.abort(StatusCode.UNAVAILABLE, details='账号或密码为空')
        await cursor.execute('insert into UserAuthBind (uid, auth, password) values (%s, %s, %s) '
                             'on duplicate key update UserAuthBind.password = password', request.uid, auth, password)


class NotificationService(notification_grpc.NotificationServicer):
    async def UpdateEventSubscribe(self, request: notification_model.UpdateEventSubscribeRequest,
                                   context: ServicerContext):
        event = NotificationEvent(request.event)
        if event == NotificationEvent.ScoreQuery:
            await _handle_update_score_query(request, context)
        await handle_subscribe_update(request.uid, event, request.is_subscribe)
        return common_model.DefaultResponse(msg='success')

    async def FetchSubscribeInfo(self, request: common_model.UserId, context: ServicerContext):
        async with NCSqlManager().cursor(DatabaseConfig.Notification) as cursor:
            await cursor.execute('select event_id from Subscribe where uid = %s', (request.uid,))
            events = await cursor.fetchall()
            result = []
            for event in events:
                temp = NotificationEvent.from_event_id(event[0]).value
                result.append(temp)
            return notification_model.FetchSubscribeInfoResponse(events=result)

