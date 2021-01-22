#! /usr/bin/python3

import psutil, sys, subprocess, os, socket

UDP_IP = "192.168.255.123"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def panic():
    with open('/home/rock64/webAPI/status', 'w') as f:
        f.write("panic")
    sock.sendto(bytes('panic', 'utf-8'), (UDP_IP, 9999))
    os.system('reboot now')


if __name__ == '__main__':
    for p in psutil.process_iter(["name"]):
        if "gunicorn3" in p.name():
            sys.exit(0)
    try:
        os.chdir("/home/rock64/homeAutomation")
        retcode = subprocess.run(["/usr/bin/gunicorn3", "--workers=4", "-D", "-b", "0.0.0.0:4500", "webAPI:app"], check=True)
        retcode.check_returncode()
    except subprocess.CalledProcessError as e:
        print("blad startu webAPI")
        #panic()
