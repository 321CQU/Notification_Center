from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from typing import ClassVar as _ClassVar, Optional as _Optional

DESCRIPTOR: _descriptor.FileDescriptor

class SetUserApnsRequest(_message.Message):
    __slots__ = ["apn", "sid"]
    APN_FIELD_NUMBER: _ClassVar[int]
    SID_FIELD_NUMBER: _ClassVar[int]
    apn: str
    sid: str
    def __init__(self, sid: _Optional[str] = ..., apn: _Optional[str] = ...) -> None: ...

class SetUserApnsResponse(_message.Message):
    __slots__ = ["msg", "status"]
    MSG_FIELD_NUMBER: _ClassVar[int]
    STATUS_FIELD_NUMBER: _ClassVar[int]
    msg: str
    status: int
    def __init__(self, status: _Optional[int] = ..., msg: _Optional[str] = ...) -> None: ...
