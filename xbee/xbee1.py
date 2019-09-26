from digi.xbee.devices import XBeeDevice

# TODO: Replace with the serial port where your local module is connected to.
PORT = "COM24"
# TODO: Replace with the baud rate of your local module.
BAUD_RATE = 9600

DATA_TO_SEND = "Hello XBee!"

# REMOTE_NODE_ID = "Proto2"  # AVR
REMOTE_NODE_ID = "ProtoX4"  # X4
# REMOTE_NODE_ID = "0013A20040326B12"  # X4
# REMOTE_NODE_ID = "0013A200403C2837"  # AVR
# REMOTE_NODE_ID = "0013A200403C283A"  # FTDI


def main():
    print(" +--------------------------------------+")
    print(" | XBee Python Library Send Data Sample |")
    print(" +--------------------------------------+\n")

    device = XBeeDevice(PORT, BAUD_RATE)

    try:
        device.open()

        def data_receive_callback(xbee_message):
            print("From {} >> {}".format(xbee_message.remote_device.get_64bit_addr(), xbee_message.data.decode()))

        device.add_data_received_callback(data_receive_callback)

        print("Waiting for data...\n")


        # Obtain the remote XBee device from the XBee network.
        xbee_network = device.get_network()
        remote_device = xbee_network.discover_device(REMOTE_NODE_ID)
        if remote_device is None:
            print("Could not find the remote device")
            exit(1)

        print("Sending data to {} >> {}...".format(remote_device.get_64bit_addr(), DATA_TO_SEND))

        device.send_data(remote_device, DATA_TO_SEND + '\r\n')

        print("Success")

        input("Press any key to quit...\n")

    finally:
        if device is not None and device.is_open():
            device.close()


if __name__ == '__main__':
    main()