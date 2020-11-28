#! /usr/bin/python3

import psutil, sys, subprocess, os, socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def reboot():
    sock.sendto(bytes('panic', 'utf-8'), (UDP_IP, 9999))
    os.system('reboot now')


if __name__ == '__main__':
    for p in psutil.process_iter():
        if "gunicorn3" in p.name():
            sys.exit(0)
    try:
        os.chdir("/home/przemek/github/dekiel/homeAutomation")
        retcode = subprocess.run(["/usr/bin/gunicorn3", "--workers=4", "-D", "-b", "0.0.0.0:4500", "webAPI:app"], check=True)
        retcode.check_returncode()
    except subprocess.CalledProcessError as e:
        print("blad restartu owserver")
        reboot()
