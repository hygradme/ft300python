from ft300python.ft300_modbusrtu import FT300ModbusRTU


if __name__ == "__main__":
    # this example is tested in Windows 10.
    # Port name would be different in other environment.
    # You can get some info of ft300 sensor with force torque values.

    port = "COM3"
    ft_modbusrtu = FT300ModbusRTU(port, timeout=1, zero_reset=False)

    print("production year", ft_modbusrtu.get_production_year())
    print("serial number", ft_modbusrtu.get_serial_number())
    print("acceralation", ft_modbusrtu.get_acceralation())
    print("force torque", ft_modbusrtu.get_force_torque())

    ft_modbusrtu.reset_zero_force_torque()
    print("reset zero force torque with current values")
    print("force torque", ft_modbusrtu.get_force_torque())

    # while True:
    #     ft_values = ft_modbusrtu.get_force_torque()
    #     print(f"["
    #           f"{ft_values[0]:0.3f}, "
    #           f"{ft_values[1]:0.3f}, "
    #           f"{ft_values[2]:0.3f}, "
    #           f"{ft_values[3]:0.3f}, "
    #           f"{ft_values[4]:0.3f}, "
    #           f"{ft_values[5]:0.3f}]")
