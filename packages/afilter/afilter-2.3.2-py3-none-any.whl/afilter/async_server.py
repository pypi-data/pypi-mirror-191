import asyncio
import sys
import grpc
import logging
import argparse
from concurrent import futures
from typing import AsyncIterable

from afilter.protos import afilter_pb2
from afilter.protos import afilter_pb2_grpc


from afilter.server import UserData, get_OKNG, get_defects, FilterServicer

try:
    from mmseg.datasets.vsp_cam import VSP_CAMDataset
    CLASSES = VSP_CAMDataset.CLASSES
except Exception as e:
    CLASSES = ('background', 'island', 'nick', 'open', 'protrusion', 'short')

if sys.version_info >= (3, 0):
    import queue
else:
    import Queue as queue

user_data = UserData()

class async_FilterServicer(FilterServicer):
    async def FilterChat(self, requests_iterator: AsyncIterable[
        afilter_pb2.OneRequest], context) -> AsyncIterable[afilter_pb2.OneReply]:
        async for request in requests_iterator:
            defects, crop_bboxes = get_defects(self.protocol.lower(), self.triton_client, 
                                               self.model_name, [request], set_async = True)
            for defect, crop_bbox in zip(defects, crop_bboxes):
                yield get_OKNG(defect, crop_bbox)


async def aivs_serve(protocol, url, model_name) -> None:
    MAX_MESSAGE_LENGTH = 256*1024*1024 # 256MB
    server = grpc.aio.server(futures.ThreadPoolExecutor(max_workers=10), options=[
               ('grpc.max_send_message_length', MAX_MESSAGE_LENGTH),
               ('grpc.max_receive_message_length', MAX_MESSAGE_LENGTH)])
    afilter_pb2_grpc.add_FilterServicer_to_server(
        async_FilterServicer(protocol, url, model_name, set_async = True), server)
    server.add_insecure_port('[::]:50051')
    await server.start()
    await server.wait_for_termination()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-u',
        '--triton_url',
        type=str,
        required=False,
        default='localhost',
        help='Inference server URL. Default is localhost.')
    parser.add_argument('-i',
        '--protocol',
        type=str,
        required=False,
        default='gRPC',
        help='Protocol (HTTP/gRPC) used to communicate with ' +
        'the inference service. Default is HTTP.')
    parser.add_argument('--model_name', default='segformer-b2', help='The model name in the server')
    args = parser.parse_args()

    logging.basicConfig()
    asyncio.get_event_loop().run_until_complete(aivs_serve(args.protocol, args.triton_url, args.model_name))
