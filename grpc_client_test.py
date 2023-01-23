import asyncio
import logging

import grpc

from notificationCenter.proto import apns_pb2, apns_pb2_grpc


async def test_set_apns(stub: apns_pb2_grpc.ApnsStub) -> None:
    # res: apns_pb2.DefaultResponse = await stub.SetUserApns(apns_pb2.SetUserApnsRequest(sid="test", apn="test"))
    # print(res)

    alert = apns_pb2.SendNotificationRequest.AppleNotification.AppleAlert(title="测试通知", subtitle="测试通知副标题",
                                                                          body="测试通知正文")
    notification = apns_pb2.SendNotificationRequest.AppleNotification(alert=alert, badge=-1, category=None)
    res2: apns_pb2.DefaultResponse = \
        await stub.SendNotificationToUser(apns_pb2.SendNotificationRequest(sid="20204051", notification=notification))
    print(res2)


async def main():
    async with grpc.aio.insecure_channel('localhost:53210') as channel:
        stub = apns_pb2_grpc.ApnsStub(channel)
        await test_set_apns(stub)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(main())
