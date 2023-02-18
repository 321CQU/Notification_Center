from micro_services_protobuf.protobuf_enum.notification_center import NotificationEvent

from _321CQU.sql_helper.SqlManager import DatabaseConfig

from utils.sqlManager import NCSqlManager


__all__ = ['handle_subscribe_update']


async def handle_subscribe_update(uid: bytes, event: NotificationEvent, is_subscribe: bool):
    async with NCSqlManager().cursor(DatabaseConfig.Notification) as cursor:
        if is_subscribe:
            sql = "insert ignore into Subscribe (uid, event_id) VALUE (%s, %s)"
        else:
            sql = "delete from Subscribe where uid = %s and event_id = %s"
        await cursor.execute(sql, (uid, event.event_id))
