import grpc
import time
from concurrent import futures

import hipnuc_usb_apiserver.grpc.imu_packet_pb2 as imu_packet_pb2
import hipnuc_usb_apiserver.grpc.imu_packet_pb2_grpc as imu_packet_pb2_grpc


class IMUPacketService(imu_packet_pb2_grpc.IMUPacketServiceServicer):
    index: int = 0

    def GetPacket(self, request, context):
        print("GetPacket", request)
        self.index += 1
        return imu_packet_pb2.IMUPacketResponse(id=self.index, timestamp=time.time_ns())

    def GetPacketArray(self, request, context):
        print("GetPacketArray", request)
        self.index += 1
        return imu_packet_pb2.IMUPacketArrayResponse(
            packets=[imu_packet_pb2.IMUPacketResponse(id=self.index, timestamp=time.time_ns()), imu_packet_pb2.IMUPacketResponse(id=self.index, timestamp=time.time_ns())])

    def GetPacketStream(self, request, context):
        print("GetPacketStream", request)
        context.add_callback(lambda: print("context deadline exceeded"))
        while True:
            if request.eof or context.is_active() == False:
                return
            else:
                self.index += 1
                yield imu_packet_pb2.IMUPacketResponse(id=self.index, timestamp=time.time_ns())


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    imu_packet_pb2_grpc.add_IMUPacketServiceServicer_to_server(
        IMUPacketService(), server)
    server.add_insecure_port('[::]:8080')
    server.start()
    try:
        while True:
            time.sleep(86400)
    except KeyboardInterrupt:
        server.stop(0)


if __name__ == '__main__':
    serve()
