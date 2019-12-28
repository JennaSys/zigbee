import socket
from time import sleep

UDP_IP = "0.0.0.0"
UDP_PORT = 5555

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind((UDP_IP, UDP_PORT))


def send_udp(msg, dest_addr):
    return sock.sendto(msg.encode(), dest_addr)


while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    print("received message: {} from {}".format(data.decode(), addr))
    # sleep(10)  # just to test for latency issues with UDP connection
    result = send_udp("data({})".format(data.decode()), addr)
    print("{} bytes sent".format(result))
