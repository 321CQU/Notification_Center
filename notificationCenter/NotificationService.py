from grpc.aio import ServicerContext

from micro_services_protobuf.notification_center import service_pb2_grpc as notification_grpc
from micro_services_protobuf.notification_center import event_pb2 as notification_model
from micro_services_protobuf import common_pb2 as common_model

from notificationCenter.subscribe import NotificationEvent, handle_subscribe_update
from utils.sqlManager import SqlManager


__all__ = ['NotificationService']


class NotificationService(notification_grpc.NotificationServicer):
    async def UpdateEventSubscribe(self, request: notification_model.UpdateEventSubscribeRequest,
                                   context: ServicerContext):
        await handle_subscribe_update(request.uid, NotificationEvent(request.event), request.is_subscribe)
        return common_model.DefaultResponse(msg='success')

    async def FetchSubscribeInfo(self, request: common_model.UserId, context: ServicerContext):
        async with SqlManager().cursor() as cursor:
            import aiomysql
            cursor: aiomysql.Cursor
            await cursor.execute('select event_id from Subscribe where uid = %s', (request.uid,))
            events = await cursor.fetchall()
            result = []
            for event in events:
                temp = NotificationEvent.from_event_id(event[0]).value
                result.append(temp)
            return notification_model.FetchSubscribeInfoResponse(events=result)

