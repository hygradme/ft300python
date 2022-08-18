import serial

from pymodbus.client.sync import ModbusSerialClient as ModbusClient


class FT300Stream:
    def __init__(self, port, timeout, zero_reset=True):
        client = ModbusClient(method = "rtu", port=port, stopbits = 1, bytesize = 8, parity = "N", baudrate= 19200, timeout=timeout)
        client.connect()

        # write 0x200 in register 410 to start data stream
        try:
            request = client.write_registers(address=410, values=0x200, unit= 9)
        finally:
            client.close()

        # start obtaining stream
        self.ser = serial.Serial(port=port, baudrate=19200, bytesize=8, parity="N", stopbits=1)
        self.STARTBYTES = bytes([0x20, 0x4e])

        #Read serial buffer until founding the bytes [0x20,0x4e]
        self.ser.reset_input_buffer()

        # ignore first several values and get value for zero calibration in the end
        for i in range(10):
            data = bytearray(self.ser.read_until(self.STARTBYTES))

        self.zero_force_torque = [0, 0, 0, 0, 0, 0]
        if zero_reset:
            self.zero_force_torque = self.get_force_torque_raw()

    def __del__(self):
        for i in range(50):
            self.ser.write([0xff])
        self.ser.close()

    def get_force_torque_raw(self):
        """get raw force and torque value without zero reset"""
        raw_bytes = bytearray(self.ser.read_until(self.STARTBYTES))
        coef_list = [100, 100, 100, 1000, 1000, 1000]
        force_torque = [int.from_bytes(raw_bytes[i*2: i*2+2], byteorder='little', signed=True) / coef_list[i] for i in range(0, 6)]
        return force_torque

    def reset_zero_force_torque(self):
        """reset zero force torque values with current force torque"""
        self.zero_force_torque = self.get_force_torque_raw()

    def get_force_torque(self):
        """get force and torque value based on zero reset ft"""
        return [ft - ft_zero for ft, ft_zero in zip(self.get_force_torque_raw(), self.zero_force_torque)]
