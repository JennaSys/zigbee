from socket import *
from select import * 
import traceback

try:
    # Create the socket, datagram mode, proprietary transport:
    sd = socket(AF_ZIGBEE, SOCK_DGRAM, ZBS_PROT_TRANSPORT)
    # Bind to endpoint 0xe8 (232) for ZB/DigiMesh, but 0x00 for 802.15.4
    sd.bind(("", 0xe8, 0, 0))
    # Configure the socket for non-blocking operation:
    sd.setblocking(0) 

    #UDP communication over ethernet
    UDP_IP = "192.168.1.48"  # UDP server
    UDP_PORT = 5555
    udp_sock = socket(AF_INET, SOCK_DGRAM)
    # udp_sock.bind(('', 55555))
    udp_sock.bind(('', 0))  # Let system get available UDP port
    udp_sock.setblocking(0) 


    # Initialize state variables:
    payload = ""
    src_addr = ()
 
    rlist = [sd, udp_sock]
    
    # Forever: 
    while True: 
        wlist = []
        if len(payload) > 0:
            wlist.append(sd)
            wlist.append(udp_sock)
            new_payload = payload

        # Block on select: 
        readable, writable, exceptions = select(rlist, wlist, []) 
        for sock in readable:
            # print "Read available"
            if sock is sd:
                # Receive from the socket:
                payload, src_addr = sd.recvfrom(72)
                print "Received '%s' from %s" % (payload, src_addr[0][1:-2])
                # If the packet was "quit", then quit:
                if payload == "quit":
                    raise Exception, "quit received"
            if sock is udp_sock:
                data, addr = udp_sock.recvfrom(1024)
                print "received UDP message: %s from %s" % (data, addr)

        for sock in writable:
            if sock is sd:
                # Send to the socket: 
                count = sd.sendto("-->"+payload+"\r", 0, src_addr)
                # Slice off count bytes from the buffer,
                # useful for if this was a partial write:
                payload = payload[count:]
            if sock is udp_sock:
                udp_sock.sendto(new_payload, (UDP_IP, UDP_PORT))

        for exc in exceptions:
            print exc


except Exception, e:
    traceback.print_exc()
    # print e
    # upon an exception, close the socket:
    sd.close()


