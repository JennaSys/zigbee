import socket
from time import sleep


def send_udp(msg):
    UDP_IP = "192.168.1.50"
    UDP_PORT = 5555

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    return sock.sendto(msg.encode(), (UDP_IP, UDP_PORT))


if __name__ == '__main__':
    for n in range(100):
        print(send_udp("This is my test {}!".format(n)))
        sleep(1)
