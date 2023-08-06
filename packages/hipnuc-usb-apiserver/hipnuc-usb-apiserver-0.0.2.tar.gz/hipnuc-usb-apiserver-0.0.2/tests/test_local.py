import grpc
import hipnuc_usb_apiserver.grpc.imu_packet_pb2 as imu_packet_pb2
import hipnuc_usb_apiserver.grpc.imu_packet_pb2_grpc as imu_packet_pb2_grpc
import time
import tqdm

def run():
    channel = grpc.insecure_channel('localhost:8080')
    stub = imu_packet_pb2_grpc.IMUPacketServiceStub(channel)
    
    response = stub.StartLocalRecording(imu_packet_pb2.IMUStartLocalRecordingRequest(
        local_path="./test_local_recording"))
    print("StartLocalRecording client received: " + str(response))

    time.sleep(3)
    response = stub.StopLocalRecording(imu_packet_pb2.IMUStoplLocalRecordingRequest())
    print("StoptLocalRecording client received: " + str(response))

if __name__ == '__main__':
    run()
