#! /usr/bin/python3

from pyownet import protocol
import socket, time, subprocess, psutil, os, logging, logging.handlers

UDP_IP = "192.168.255.123"

# stary adres ds1820 z lazienka gora: /28.FF2B55761801

sensors = [('/28.8AAB110B0000/', 'grupa_mieszajaca', 9911), ('/28.AAE0F3521401/','zewnatrz', 9900), ('/28.FF6000691803/', 'radiostacja', 9901), ('/28.FF045C6E1801/', 'wc_dol', 9904), ('/28.FF9C5D6E1801/', 'sypialnia_lazienka',9909), ('/28.FFE35D6E1801/', 'salon_stol', 9906), ('/26.21AF930100007E/', 'lazienka_gora', 9910, 9912), ('/28.FF3B576E1801/', 'przedpokoj', 9905), ('/28.FFFB01691803/', 'salon_kanapa', 9907), ('/28.FFC703691803/', 'gabinet', 9908), ('/28.FF575B6E1801/', 'lazienka_dol', 9903), ('/28.FF5F576E1801/', 'czikita', 9902)]

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def panic():
    with open('/home/rock64/webAPI/status', 'w') as f:
        f.write("panic")
    sock.sendto(bytes('panic', 'utf-8'), (UDP_IP, 9999))
    my_logger.critical("owserver niedostepny, restartuje system")
    os.system('reboot now')

if __name__ == '__main__':
    my_logger = logging.getLogger('sysloger')
    my_logger.setLevel(logging.DEBUG)

    handler = logging.handlers.SysLogHandler(address='/dev/log')

    my_logger.addHandler(handler)
    count = 2
    while count > 1:
        count = 0
        for p in psutil.process_iter(["name"]):
            if "oneWireBus" in p.name():
                count += 1
                if count > 2:
                    my_logger.critical("dziala wiecej niz dwa procesy odczytu temperatury")
                    panic()
    time.sleep(5)

    try:
        owproxy = protocol.proxy(host="127.0.0.1", port=4304)
        for sensor in sensors:
            if owproxy.present(sensor[0]):
                if sensor[1] == 'lazienka_gora':
                    value = (owproxy.read('%stemperature' % sensor[0]).decode('utf-8').strip())
                    humidity = (owproxy.read('%shumidity' % sensor[0]).decode('utf-8').strip())
                    sock.sendto(bytes(value, 'utf-8'), (UDP_IP, sensor[2]))
                    sock.sendto(bytes(humidity, 'utf-8'), (UDP_IP, sensor[3]))
                else:
                    value = (owproxy.read('%stemperature10' % sensor[0]).decode('utf-8').strip())
                    time.sleep(1)
                    sock.sendto(bytes(value, 'utf-8'),(UDP_IP, sensor[2]))
                #my_logger.info("Read tmp for {}".format(sensor[1]))
            else:
                my_logger.critical("Blad odczytu czujnika, restartuje owserver")
                try:
                    retcode = subprocess.run(["/bin/systemctl", "restart", "owserver.service"], check=True)
                    retcode.check_returncode()
                    time.sleep(5)
                    if owproxy.present(sensor[0]):
                        if sensor[1] == 'lazienka_gora':
                            value = (owproxy.read('%stemperature' % sensor[0]).decode('utf-8').strip())
                            humidity = (owproxy.read('%shumidity' % sensor[0]).decode('utf-8').strip())
                            sock.sendto(bytes(value, 'utf-8'), (UDP_IP, sensor[2]))
                            sock.sendto(bytes(humidity, 'utf-8'), (UDP_IP, sensor[3]))
                        else:
                            value = (owproxy.read('%stemperature10' % sensor[0]).decode('utf-8').strip())
                            sock.sendto(bytes(value, 'utf-8'), (UDP_IP, sensor[2]))
                    else:
                        my_logger.critical("Czujnik {} nadal nie dostepny".format(sensor[1]))
                        panic()
                except subprocess.CalledProcessError as e:
                    my_logger.critical("blad restartu owserver")
                    panic()
    #except pyownet.protocol.OwnetError:
    except:
        try:
            retcode = subprocess.run(["/bin/systemctl", "restart", "owserver.service"], check=True)
            retcode.check_returncode()
            time.sleep(5)
        except subprocess.CalledProcessError as e:
            my_logger.critical("blad restartu owserver")
            panic()

