# ARIZON USB APIServer

![Upload Python Package](https://github.com/mvig-robotflow/arizon_usb_apiserver/workflows/Upload%20Python%20Package/badge.svg)
[![Pypi](https://img.shields.io/pypi/v/arizon_usb_apiserver.svg)](https://pypi.org/project/arizon_usb_apiserver/)

An APIServer for ARIZON USB force sensors.

## Installation

Clone & `cd` into this repository then:

```shell
python setup.py install
```

Or download from PyPI:

```shell
python -m pip install arizon-usb-apiserver
```

## Get Started

The apiserver operates in two modes: RESTful and gRPC. They share the same configuration schema.

### Basics

To read the sensor locally, use this snippet:

```python
from serial import Serial
from arizon_usb_apiserver import Sensor

if __name__ == '__main__':
    conn = Serial("COM16", 115200)
    sensor = Sensor(conn)
    sensor.reset()
    while True:
        print(sensor.read_once())
```

To generate configuration from command line interaction run:

```shell
python -m arizon_usb_apiserver configure
```

### RESTful

To launch the apiserver in RESTful mode, set the `API_SERVER_RESTFUL` to `1` before run:


```shell
export API_SERVER_RESTFUL=1
```

Or run with variable

```shell
API_SERVER_RESTFUL=1 python -m arizon_usb_apiserver apiserver
```

> Powershell: `Set-Item -Path Env:API_SERVER_RESTFUL -Value 1`

Init sensor

```shell
curl -X 'PUT' \
  'http://127.0.0.1:8080/v1/arizon/force?flag=true' \
  -H 'accept: application/json'
```

Read sensor

```shell
curl -X 'GET' \
  'http://127.0.0.1:8080/v1/arizon/force' \
  -H 'accept: application/json'
```

Shutdown sensor

```shell
curl -X 'PUT' \
  'http://127.0.0.1:8080/v1/arizon/force?flag=false' \
  -H 'accept: application/json'
```

## gRPC

Run this command

```shell
python -m arizon_usb_apiserver apiserver
```

## Generate Client

### Restful

First launch the apiserver, then run `openapi-python-client`:

```shell
openapi-python-client generate --url http://127.0.0.1:8080/openapi.json
rm -rf ./arizon_usb_driver/client/restful
mv fast-api-client/fast_api_client ./arizon_usb_driver/client/restful
rm -rf ./fast-api-client
```

### GRPC

First `cd arizon_usb_apiserver/grpc`, then run:

```shell
python -m grpc_tools.protoc -I../../manifests/protos --python_out=. --pyi_out=. --grpc_python_out=. ../../manifests/protos/force_packet.proto
```

You might need to replace `import force_packet_pb2 as force__packet__pb2` with `import arizon_usb_apiserver.grpc.force_packet_pb2 as force__packet__pb2`

## Serial Protocol

| Field        | Content |
| ------------ | ------- |
| Head         | 0xFE    |
| Status       | 1 Byte  |
| Data         | 3 Byte  |
| XOR checksum | 1 Byte  |

- Status: 4 bits of address + 4 bits represents number of digits
- Data: 3 bytes of signed integers, no digit, big-endian.
- Checksum: xor() of first 5 bytes
