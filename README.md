# ft300python

## Summary
Python module to obtain sensor values from ROBOTIQ FT300 Force Torque Sensor.

See an official manual for details of FT300:

https://assets.robotiq.com/website-assets/support_documents/document/FT_Sensor_Instruction_Manual_PDF_20181218.pdf

## installation
```
pip install ft300python
```

## Dependencies
- pyserial
- pymodbus

## Usage
See test_ft300_modbusrtu.py and test_ft300_stream.py in examples/

For higher frequency application, use ft300_stream.