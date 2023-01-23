from typing import Union, Optional

from pydantic import BaseModel, Field

__all__ = ['AppleAlert', 'AppleNotification']


class AppleAlert(BaseModel):
    """
    Apple应用通知消息内容
    """
    title: str = Field(description='通知标题')
    sub_title: str = Field(alias='sub-title', description='通知副标题')
    body: str = Field(description='通知正文')


class AppleNotification(BaseModel):
    """
    Apple APNs请求字典
    """
    alert: Optional[Union[AppleAlert, str]] = Field(description='显示警报的信息。建议使用字典。如果您指定字符串，警报会将您的字符串显示为正文文本')
    badge: Optional[int] = Field(description='应用程序图标上徽章中显示的数字。指定0以删除当前徽章（如果有的话）')
    category: Optional[str] = Field(description='通知的类型')
