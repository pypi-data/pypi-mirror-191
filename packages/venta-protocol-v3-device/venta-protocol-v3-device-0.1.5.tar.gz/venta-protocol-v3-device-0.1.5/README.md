Library to control Venta Air Humidifiers that use Protol Version 3 (via REST API on Port 80) 

Example usage:
``` { .py }
from venta_protocol_v3_device import Venta_Protocol_v3_Device

d = Venta_Protocol_v3_Device("192.168.178.87")
d.getStatus()

print(d.toJSON())
```