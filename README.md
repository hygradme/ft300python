# ft300python

## Summary
Python module to obtain sensor values from ROBOTIQ FT300 Force Torque Sensor.

See an official manual for details of FT300:

https://assets.robotiq.com/website-assets/support_documents/document/FT_Sensor_Instruction_Manual_PDF_20181218.pdf

## Installation
```
pip install ft300python
```

## Dependencies
- pyserial
- pymodbus

## Usage
See test_ft300_modbusrtu.py and test_ft300_stream.py in examples/

### Modbus RTU version (About 30Hz data acquisition):
```
from ft300python.ft300_modbusrtu import FT300ModbusRTU


port = "COM3"
ft_modbusrtu = FT300ModbusRTU(port, timeout=1, zero_reset=False)

print("production year", ft_modbusrtu.get_production_year())
print("serial number", ft_modbusrtu.get_serial_number())
print("acceralation", ft_modbusrtu.get_acceralation())
print("force torque", ft_modbusrtu.get_force_torque())

ft_modbusrtu.reset_zero_force_torque()
print("reset zero force torque with current values")
print("force torque", ft_modbusrtu.get_force_torque())
```

### Data Stream version (About 100Hz data acquisition):
```
from ft300python.ft300_stream import FT300Stream


port = "COM3"
ft_stream = FT300Stream(port, timeout=1, zero_reset=True)

while True:
    ft_values = ft_stream.get_force_torque()
    print(ft_values)
```