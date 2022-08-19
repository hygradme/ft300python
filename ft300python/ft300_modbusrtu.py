from pymodbus.client.sync import ModbusSerialClient as ModbusClient


def uint_to_int(register):
    register_bytes = register.to_bytes(2, byteorder='little')
    return int.from_bytes(register_bytes, byteorder='little', signed=True)


class FT300ModbusRTU:
    def __init__(self, port, timeout, zero_reset=True):
        self.client = ModbusClient(
            method="rtu",
            port=port,
            stopbits=1,
            bytesize=8,
            parity="N",
            baudrate=19200,
            timeout=1
            )
        self.client.connect()
        self.register_dict = {
            "ProductionYear": 514,
            "SerialNumber0": 510,
            "SerialNumber1": 511,
            "SerialNumber2": 512,
            "SerialNumber3": 513,
            "F_x": 180,
            "F_y": 181,
            "F_z": 182,
            "M_x": 183,
            "M_y": 184,
            "M_z": 185,
            "acc_x": 190,
            "acc_y": 191,
            "acc_z": 192
        }
        self.value_coef_list = [100, 100, 100, 1000, 1000, 1000]
        self.acc_coef_list = [1000, 1000, 1000]

        self.zero_force_torque = [0, 0, 0, 0, 0, 0]
        if zero_reset:
            self.zero_force_torque = self.get_force_torque_raw()

    def __del__(self):
        self.client.close()

    def get_force_torque_raw(self):
        result = self.client.read_holding_registers(
            address=self.register_dict["F_x"], count=6, unit=9)
        force_torque = [uint_to_int(ft) / coef for ft, coef
                        in zip(result.registers, self.value_coef_list)]
        return force_torque

    def reset_zero_force_torque(self):
        """reset zero force torque values with current force torque"""
        self.zero_force_torque = self.get_force_torque_raw()

    def get_force_torque(self):
        """get force and torque value based on zero reset ft"""
        return [ft - ft_zero for ft, ft_zero
                in zip(self.get_force_torque_raw(), self.zero_force_torque)]

    def get_acceralation(self):
        """get acceleration values"""
        result = self.client.read_holding_registers(
            address=self.register_dict["acc_x"], count=3, unit=9)
        acc_list = [uint_to_int(acc) / coef for acc, coef
                    in zip(result.registers, self.acc_coef_list)]
        return acc_list

    def get_production_year(self):
        result = self.client.read_holding_registers(
            address=self.register_dict["ProductionYear"], count=1, unit=9)
        return result.registers[0]

    def get_serial_number(self):
        result = self.client.read_holding_registers(
            address=self.register_dict["SerialNumber0"], count=4, unit=9)
        return result.registers

    def disconnect(self):
        self.client.close()
