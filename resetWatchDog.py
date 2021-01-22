#! /usr/bin/python3

import socket

UDP_IP = "192.168.255.123"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if __name__ == '__main__':
    sock.sendto(bytes('live', 'utf-8'), (UDP_IP, 9999))
    with open('/home/rock64/webAPI/status', 'w') as f:
        f.write("live")