import grpc
import time
import tqdm

import hipnuc_usb_apiserver.grpc.imu_packet_pb2 as imu_packet_pb2
import hipnuc_usb_apiserver.grpc.imu_packet_pb2_grpc as imu_packet_pb2_grpc


def run():
    channel = grpc.insecure_channel('localhost:8080')
    stub = imu_packet_pb2_grpc.IMUPacketServiceStub(channel)

    response = stub.SetFIFOStatus(imu_packet_pb2.IMUSetFIFOStatusRequest(
        status=True))
    print("SetStatus client received: " + str(response))

    response = stub.GetPacket(imu_packet_pb2.IMUPacketRequest(
        timestamp=time.time_ns()))
    print("GetPacket client received: " + str(response))

    response = stub.GetPacketArray(
        imu_packet_pb2.IMUPacketArrayRequest(timestamp=time.time_ns()))
    print("GetPacketArray client received: " + str(response))

    response = stub.GetPacketStream(
        imu_packet_pb2.IMUPacketRequest(timestamp=time.time_ns()))
    print("GetPacketStream client received: " + str(response))

    try:
        with tqdm.tqdm() as pbar:
            while True:
                # time.sleep(0.0005)
                data = next(response)
                pbar.set_description(str(data.yaw) + ' - ' + str(data.index))
                pbar.update(1)
                # print)
    except KeyboardInterrupt as e:
        response.cancel()

    response = stub.SetFIFOStatus(imu_packet_pb2.IMUSetFIFOStatusRequest(
        status=False))
    print("SetStatus client received: " + str(response))


if __name__ == '__main__':
    run()
