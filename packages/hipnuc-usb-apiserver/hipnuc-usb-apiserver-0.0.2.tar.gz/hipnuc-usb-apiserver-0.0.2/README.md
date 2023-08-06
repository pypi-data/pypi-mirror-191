# HIPNUC USB APIServer

![Upload Python Package](https://github.com/mvig-robotflow/arizon_usb_apiserver/workflows/Upload%20Python%20Package/badge.svg)
[![Pypi](https://img.shields.io/pypi/v/arizon_usb_apiserver.svg)](https://pypi.org/project/arizon_usb_apiserver/)

## Installation

Clone & `cd` into this repository then:

```shell
python setup.py install
```

Or download from PyPI:

```shell
python -m pip install hipnuc-usb-apiserver
```

## Get Started

To generate configuration from command line interaction run:

```shell
python -m hipnuc_usb_apiserver configure
```

To launch the apiserver, run:

```shell
python -m hipnuc_usb_apiserver apiserver
```

To use the gRPC api on `localhost:8080`, use this snippet:

```python
import grpc
import hipnuc_usb_apiserver.grpc.imu_packet_pb2 as imu_packet_pb2
import hipnuc_usb_apiserver.grpc.imu_packet_pb2_grpc as imu_packet_pb2_grpc
import time
import tqdm

def run():
    channel = grpc.insecure_channel('localhost:8080')
    stub = imu_packet_pb2_grpc.IMUPacketServiceStub(channel)
    
    response = stub.SetStatus(imu_packet_pb2.IMUSetStatusRequest(
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
    
    response = stub.SetStatus(imu_packet_pb2.IMUSetStatusRequest(
    status=False))
    print("SetStatus client received: " + str(response))


if __name__ == '__main__':
    run()
```

> for custom port configuration, change the `localhost:8080`

## Developping

For developping purpose, read this section.

### Build gRPC

To update gRPC defs, run:

```shell
cd hipnuc_usb_apiserver/grpc
python -m grpc_tools.protoc -I../../manifests/protos --python_out=. --pyi_out=. --grpc_python_out=. ../../manifests/protos/imu_packet.proto
```
