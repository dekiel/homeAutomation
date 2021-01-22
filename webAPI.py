from flask import Flask
app = Flask(__name__)

webAPIRoot = "/home/rock64"

def heaterON(gpionr, room):
    with open('/sys/class/gpio/gpio{}/value'.format(gpionr), 'w') as f:
        f.write("1")
    return '{}: ogrzewanie wlaczone'.format(room)


def heaterOFF(gpionr, room):
    with open('/sys/class/gpio/gpio{}/value'.format(gpionr), 'w') as f:
        f.write("0")
    return '{}: ogrzewanie wlaczone'.format(room)


@app.route('/areyoualive')
def areyoualive():
    with open('{}/webAPI/status'.format(webAPIRoot)) as f:
        return f.read().split('\n')[0]


@app.route('/gabinet-on')
def gabinetOn():
    return heaterON(99, "gabinet")
@app.route('/gabinet-off')
def gabinetOff():
    return heaterOFF(99, "gabinet")


@app.route('/przedpokoj-on')
def przepokojON():
    return heaterON(83, "przedpokoj")
@app.route('/przedpokoj-off')
def przedpokojOff():
    return heaterOFF(83, "przedpokoj")


@app.route('/zosia-on')
def zosiaON():
    return heaterON(80, "zosia")
@app.route('/zosia-off')
def zosiaOFF():
    return heaterOFF(80, "zosia")

@app.route('/sypialnia-on')
def sypialniaON():
    return heaterON(79, "sypialnia")
@app.route('/sypialnia-off')
def gabinetOff():
    return heaterOFF(79, "sypialnia")

@app.route('/gabinet-status')
def gabinetStatus():
    with open('/sys/class/gpio/gpio102/value') as f:
        status = f.read()
    if status.split('\n')[0] == "1":
        return "ogrzewanie w gabinecie jest wlaczone"
    if status.split('\n')[0] == "0":
        return "ogrzewanie w gabinecie jest wylaczone"
    return "status ogrzewania w gabinecie nieznany"