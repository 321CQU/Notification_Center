from typing import Union, Optional

from pydantic import BaseModel, Field

from micro_services_protobuf.notification_center.apns_pb2 import SendNotificationRequest

__all__ = ['AppleAlert', 'AppleNotification']


class AppleAlert(BaseModel):
    """
    Apple应用通知消息内容
    """
    title: str = Field(description='通知标题')
    subtitle: str | None = Field(description='通知副标题')
    body: str = Field(description='通知正文')

    @staticmethod
    def from_proto(obj: SendNotificationRequest.AppleNotification.AppleAlert):
        return AppleAlert(title=obj.title, subtitle=obj.subtitle if obj.subtitle != '' else None, body=obj.body)


class AppleNotification(BaseModel):
    """
    Apple APNs请求字典
    """
    alert: Optional[Union[AppleAlert, str]] = Field(description='显示警报的信息。建议使用字典。如果您指定字符串，警报会将您的字符串显示为正文文本')
    badge: Optional[int] = Field(description='应用程序图标上徽章中显示的数字。指定0以删除当前徽章（如果有的话）')
    category: Optional[str] = Field(description='通知的类型')

    @staticmethod
    def from_proto(obj: SendNotificationRequest.AppleNotification):
        return AppleNotification(alert=AppleAlert.from_proto(obj.alert), badge=obj.badge if obj.badge != -1 else None,
                                 category=obj.category if obj.category != '' else None)

    def launch_request(self) -> dict:
        return {
            "aps": self.dict(exclude_none=True)
        }
