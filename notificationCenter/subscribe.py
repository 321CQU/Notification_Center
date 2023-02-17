from enum import Enum

from micro_services_protobuf.protobuf_enum.notification_center import NotificationEvent

from utils.sqlManager import SqlManager


__all__ = ['handle_subscribe_update']


async def handle_subscribe_update(uid: bytes, event: NotificationEvent, is_subscribe: bool):
    async with SqlManager().cursor() as cursor:
        sql: str
        if is_subscribe:
            await cursor.execute('select uid from Subscribe where uid = %s and event_id = %s', (uid, event.event_id))
            if (await cursor.fetchone()) is not None:
                return
            sql = "insert into Subscribe (uid, event_id) VALUE (%s, %s)"
        else:
            sql = "delete from Subscribe where uid = %s and event_id = %s"
        await cursor.execute(sql, (uid, event.event_id))
