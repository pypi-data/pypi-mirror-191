# ECMind blue client: Object Definition (objdef)

Helper modules for the `ecmind_blue_client` to ease the work with object definition APIs. See discussion here: https://hub.ecmind.ch/t/119

## Installation

`pip install ecmind_blue_client_objdef`

## Usage

```python
from ecmind_blue_client.tcp_client import TcpClient as Client
from ecmind_blue_client_objdef import objdef

client = Client(hostname='localhost', port=4000, appname='test', username='root', password='optimal')
asobjdef = objdef.load_object_definition(client)
for cabinet in asobjdef.cabinets:
    print(cabinet)
```

## Changes

### Version `0.0.3`

- Workaround and warn message for pages without internal name.

### Version `0.0.4`

- Workaround and warn message for tables without columns.

### Version `0.0.5`

- Workaround and warn message for tab pages without controls.
