# This example gives a simple demonstration of how
# to set and use ZigBee sockets configured for
# non-blocking I/O with select. This application
# echoes packets back to the originator.
# 
# The socket is marked for reading only if
# the payload buffer is empty; if the buffer is
# non-empty then the socket is marked for writing.
# Select is used to arbitrate when a socket is 
# ready to be read or written.
# 
# This example could be easily extended to operate
# on multiple sockets.
# 
 
 
# Include the socket and select modules: 
from socket import *
from select import * 
 
 
# Create the socket, datagram mode, proprietary transport:
sd = socket(AF_ZIGBEE, SOCK_DGRAM, ZBS_PROT_TRANSPORT)
# Bind to endpoint 0xe8 (232) for ZB/DigiMesh, but 0x00 for 802.15.4
sd.bind(("", 0xe8, 0, 0))
# Configure the socket for non-blocking operation:
sd.setblocking(0) 

 
try:
    # Initialize state variables:
    payload = ""
    src_addr = ()
 
    # Forever: 
 
    while 1: 
        # Reset the ready lists:
        rlist, wlist = ([], [])
        if len(payload) == 0:
 

            # If the payload buffer is empty,
            # add socket to read list: 
            rlist = [sd]
 
        else: 
            # Otherwise, add the socket to the
            # write list: 
            wlist = [sd] 
 
 
        # Block on select: 
        rlist, wlist, xlist = select(rlist, wlist, []) 
 
 
        # Is the socket readable? 
        if sd in rlist: 
            # Receive from the socket:
            payload, src_addr = sd.recvfrom(72)
            # If the packet was "quit", then quit:
            if payload == "quit": 
                raise Exception, "quit received"

        # Is the socket writable? 
        if sd in wlist: 
            # Send to the socket: 
            count = sd.sendto("-->"+payload+"\r", 0, src_addr)
            # Slice off count bytes from the buffer,
            # useful for if this was a partial write:
            payload = payload[count:]
 
except Exception, e:
    # upon an exception, close the socket:
    sd.close()


