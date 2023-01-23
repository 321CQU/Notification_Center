import asyncio
import logging

import grpc

from notificationCenter.proto import apns_pb2, apns_pb2_grpc


async def test_set_apns(stub: apns_pb2_grpc.SetUserApnsStub) -> None:
    res: apns_pb2.SetUserApnsResponse = await stub.SetUserApns(apns_pb2.SetUserApnsRequest(sid="test", apn="test"))
    print(res)


async def main():
    async with grpc.aio.insecure_channel('localhost:50051') as channel:
        stub = apns_pb2_grpc.SetUserApnsStub(channel)
        await test_set_apns(stub)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.get_event_loop().run_until_complete(main())
