import grpc
import logging
import threading
import time
from concurrent import futures
from typing import Optional, List

import hipnuc_usb_apiserver.grpc.imu_packet_pb2 as imu_packet_pb2
import hipnuc_usb_apiserver.grpc.imu_packet_pb2_grpc as imu_packet_pb2_grpc
from hipnuc_usb_apiserver.Config import Config as IMUConfig
from .app import Application

logger = logging.getLogger("hipnuc.server")


def create_packet(msg: dict) -> imu_packet_pb2.IMUPacketResponse:
    if msg is None:
        return imu_packet_pb2.IMUPacketResponse(valid=False)
    else:
        data: dict = msg['data']
        return imu_packet_pb2.IMUPacketResponse(
            id=str(data['id'][0]),
            dev_ts_ms=int(data['timestamp'][0]['(s)'] * 1000),
            accel_x=data['acc'][0]['X'],
            accel_y=data['acc'][0]['Y'],
            accel_z=data['acc'][0]['Z'],
            gyro_x=data['gyr'][0]['X'],
            gyro_y=data['gyr'][0]['Y'],
            gyro_z=data['gyr'][0]['Z'],
            mag_x=data['mag'][0]['X'],
            mag_y=data['mag'][0]['Y'],
            mag_z=data['mag'][0]['Z'],
            quat_w=data['quat'][0]['W'],
            quat_x=data['quat'][0]['X'],
            quat_y=data['quat'][0]['Y'],
            quat_z=data['quat'][0]['Z'],
            pitch=data['euler'][0]['Pitch'],
            roll=data['euler'][0]['Roll'],
            yaw=data['euler'][0]['Yaw'],
            uart_buffer_len=-1,
            index=msg['index'],
            sys_ts_ns=msg['ts_ns'],
            valid=True
        )


def create_packet_array(msg_array: List[dict]) -> imu_packet_pb2.IMUPacketResponse:
    return imu_packet_pb2.IMUPacketArrayResponse(packets=[create_packet(data) for data in msg_array])


def create_packet_sequence(msg_array: List[dict]) -> imu_packet_pb2.IMUPacketResponse:
    return imu_packet_pb2.IMUPacketSequenceResponse(packets=[create_packet(data) for data in msg_array])


class IMUPacketService(imu_packet_pb2_grpc.IMUPacketServiceServicer):
    def __init__(self, config: IMUConfig) -> None:
        super().__init__()
        self.app: Application = Application(config)
        self.app.start_thread()

    def GetFIFOStatus(self, request: imu_packet_pb2.IMUGetFIFOStatusRequest, context):
        logger.debug("GetFIFOStatus:", request)
        return imu_packet_pb2.IMUStatusResponse(status=self.app.fifo_status)

    def SetFIFOStatus(self, request: imu_packet_pb2.IMUSetFIFOStatusRequest, context):
        logger.debug("SetFIFOStatus:", request)
        if request.status:
            err = self.app.start_fifo()
        else:
            err = self.app.stop_fifo()
        return imu_packet_pb2.IMUStatusResponse(status=self.app.fifo_status, err=str(err))

    def GetPacket(self, request: imu_packet_pb2.IMUPacketRequest, context):
        logger.debug("GetPacket:", request)
        return create_packet(self.app.get_by_index(request.index))

    def GetPacketArray(self, request: imu_packet_pb2.IMUPacketArrayRequest, context):
        logger.debug("GetPacketArray:", request)
        return create_packet_array(self.app.get())

    def GetPacketSequnce(self, request: imu_packet_pb2.IMUPacketSequenceRequest, context):
        logger.debug("GetPacketSequence:", request)
        data_array = [self.app.get_by_index(
            request.index) for _ in range(request.num_packets)]
        return create_packet_sequence(data_array)

    def GetPacketArraySequence(self, request: imu_packet_pb2.IMUPacketArraySequenceRequest, context):
        logger.debug("GetPacketArraySequence:", request)
        data_sequence = [create_packet_array(
            self.app.get()) for _ in range(request.num_packets)]
        return imu_packet_pb2.IMUPacketArraySequenceResponse(packets=data_sequence)

    def GetPacketStream(self, request: imu_packet_pb2.IMUPacketRequest, context):
        logger.debug("GetPacketStream:", request)
        context.add_callback(lambda: logger.info(
            "GetPacketStream: context deadline exceeded"))
        while True:
            if context.is_active() == False:
                return
            else:
                yield create_packet(self.app.get_by_index(request.index))

    def GetPacketArrayStream(self, request: imu_packet_pb2.IMUPacketArrayRequest, context):
        logger.debug("GetPacketArrayStream:", request)
        context.add_callback(lambda: logger.info(
            "GetPacketArrayStream: context deadline exceeded"))
        while True:
            if context.is_active() == False:
                return
            else:
                yield create_packet_array(self.app.get())

    def StartLocalRecording(self, request: imu_packet_pb2.IMUStartLocalRecordingRequest, context):
        logger.debug("StartLocalRecording:", request)
        err = self.app.start_local(request.local_path)
        return imu_packet_pb2.IMUStatusResponse(status=self.app.local_status, err=str(err))

    def StopLocalRecording(self, request, context):
        logger.debug("StopLocalRecording:", request)
        err = self.app.stop_local()
        return imu_packet_pb2.IMUStatusResponse(status=self.app.local_status, err=str(err))


def get_server(cfg: IMUConfig):
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    imu_packet_pb2_grpc.add_IMUPacketServiceServicer_to_server(
        IMUPacketService(cfg), server)
    server.add_insecure_port(f'{cfg.api_interface}:{cfg.api_port}')
    return server
