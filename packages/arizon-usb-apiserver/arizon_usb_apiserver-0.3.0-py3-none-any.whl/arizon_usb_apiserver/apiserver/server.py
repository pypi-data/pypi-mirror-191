import grpc
import logging
from concurrent import futures
from typing import List

import arizon_usb_apiserver.grpc.force_packet_pb2 as force_packet_pb2
import arizon_usb_apiserver.grpc.force_packet_pb2_grpc as force_packet_pb2_grpc
from arizon_usb_apiserver.Config import Config as SensorConfig
from arizon_usb_apiserver.apiserver.app import Application

logger = logging.getLogger("hipnuc.server")


def create_packet(data: dict):
    if data is None:
        return force_packet_pb2.ForcePacketResponse(valid=False)
    else:
        return force_packet_pb2.ForcePacketResponse(**data, valid=True)


class ForcePacketService(force_packet_pb2_grpc.ForcePacketService):
    def __init__(self, config: SensorConfig) -> None:
        super().__init__()
        self.app: Application = Application(config)
        self.app.logger.info(f"arizon sensor service listen at {config.api_port}")
        self.app.logger.info(f"arizon sensor config {config}")
        self.app.start_thread()

    def GetFIFOStatus(self, request: force_packet_pb2.ForceGetFIFOStatusRequest, context):
        return force_packet_pb2.ForceStatusResponse(status=self.app.fifo_status)

    def SetFIFOStatus(self, request: force_packet_pb2.ForceSetFIFOStatusRequest, context):
        logger.info(f"SetFIFOStatus: {request}")
        if request.status:
            err = self.app.start_fifo()
        else:
            err = self.app.stop_fifo()
        return force_packet_pb2.ForceStatusResponse(status=True, err=str(err))

    def GetPacket(self, request: force_packet_pb2.ForcePacketRequest, context):
        logger.info(f"GetForcePacket: {request}")
        data = self.app.get()
        return create_packet(data)

    def GetPacketStream(self, request: force_packet_pb2.ForcePacketRequest, context):
        logger.info(f"GetForcePacketStream: {request}")
        context.add_callback(lambda: logger.info(
            "GetPacketStream: context deadline exceeded"))
        while True:
            data = self.app.get()
            # print(data)
            yield create_packet(data)

    def ResetPacketCache(self, request: force_packet_pb2.ForcePacketRequest, context):
        logger.info(f"ResetForcePacketCache: {request}")
        self.app.force_data_queue.queue.clear()
        return force_packet_pb2.ForceStatusResponse(status=True, err=str(None))


def get_server(cfg: SensorConfig):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    force_packet_pb2_grpc.add_ForcePacketServiceServicer_to_server(
        ForcePacketService(cfg), server)
    server.add_insecure_port(f'{cfg.api_interface}:{cfg.api_port}')
    return server


if __name__ == '__main__':
    import time

    server = get_server(SensorConfig('./arizon_config.yaml'))
    server.start()

    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)
