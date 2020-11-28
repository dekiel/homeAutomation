#! /usr/bin/python3

from pyownet import protocol
import socket, time, subprocess, psutil, os

UDP_IP = "192.168.255.123"

sensors = [('/28.8AAB110B0000/', 'grupa_mieszajaca', 9911), ('/28.AAE0F3521401/','zewnatrz', 9900), ('/28.FF6000691803/', 'radiostacja', 9901), ('/28.FF045C6E1801/', 'wc_dol', 9904), ('/28.FF9C5D6E1801/', 'sypialnia_lazienka',9909), ('/28.FFE35D6E1801/', 'salon_stol', 9906), ('/28.FF2B55761801/', 'lazienka_gora', 9910), ('/28.FF3B576E1801/', 'przedpokoj', 9905), ('/28.FFFB01691803/', 'salon_kanapa', 9907), ('/28.FFC703691803/', 'gabinet', 9908), ('/28.FF575B6E1801/', 'lazienka_dol', 9903), ('/28.FF5F576E1801/', 'czikita', 9902)]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

if __name__ == '__main__':
    count = 2
    while count > 1:
        count = 0
        for p in psutil.process_iter():
            if "python3" in p.name():
                count=+count
                if count > 2:
                    sock.sendto(bytes('panic', 'utf-8'), (UDP_IP, 9999))
                    os.system('reboot now')
    time.sleep(5)

    owproxy = protocol.proxy(host="127.0.0.1", port=4304)
    for sensor in sensors:
        present = owproxy.present(sensor[0])
        if present:
            value = (owproxy.read('%stemperature10' % sensor[0]).decode('utf-8').strip())
            time.sleep(1)
            sock.sendto(bytes(value, 'utf-8'),(UDP_IP, sensor[2]))
            sock.sendto(bytes('ok', 'utf-8'), (UDP_IP, 9998))
        else:
            print("Blad odczytu czujnika, restartuje owserver")
            try:
                retcode = subprocess.run(["systemctl", "restart", "owserver.service"], check=True)
                retcode.check_returncode()
                value = (owproxy.read('%stemperature10' % sensor[0]).decode('utf-8').strip())
                sock.sendto(bytes(value, 'utf-8'), (UDP_IP, sensor[2]))
            except subprocess.CalledProcessError as e:
                print("blad restartu owserver")