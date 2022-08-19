from ft300python.ft300_stream import FT300Stream


if __name__ == "__main__":
    # ft300_stream usually provides force torque values with higher frequency
    # this example is tested in Windows 10.
    # Port name would be different in other environment.

    port = "COM3"
    ft_stream = FT300Stream(port, timeout=1, zero_reset=True)

    while True:
        ft_values = ft_stream.get_force_torque()
        print(f"["
              f"{ft_values[0]:0.3f}, "
              f"{ft_values[1]:0.3f}, "
              f"{ft_values[2]:0.3f}, "
              f"{ft_values[3]:0.3f}, "
              f"{ft_values[4]:0.3f}, "
              f"{ft_values[5]:0.3f}]")
