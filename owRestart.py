#! /usr/bin/python3

import socket, time, subprocess, psutil, os, logging, logging.handlers

UDP_IP = "192.168.255.123"

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def panic():
    with open('/home/rock64/webAPI/status', 'w') as f:
        f.write("panic")
    sock.sendto(bytes('panic', 'utf-8'), (UDP_IP, 9999))
    my_logger.critical("rebooting system")
    os.system('reboot now')

if __name__ == '__main__':
    my_logger = logging.getLogger('sysloger')
    my_logger.setLevel(logging.DEBUG)

    handler = logging.handlers.SysLogHandler(address='/dev/log')

    my_logger.addHandler(handler)

    present = True
    while present :
      for p in psutil.process_iter(["name"]):
        if "oneWireBus" in p.name():
          present = True
          my_logger.info('oneWireBus process present, sleeping for 10 seconds')
        else:
          present = False
      time.sleep(10)
    try:
      retcode = subprocess.run(["/bin/systemctl", "restart", "owserver.service"], check=True)
      retcode.check_returncode()
      my_logger.info("owserver restarted")
    except subprocess.CalledProcessError as e:
      my_logger.critical("blad restartu owserver")
      panic()