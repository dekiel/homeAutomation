from flask import Flask
app = Flask(__name__)

webAPIRoot = "/home/rock64/webAPI"

def heaterON(gpionr, room):
    with open('/sys/class/gpio/gpio{}/value'.format(gpionr), 'w') as f:
        f.write("1")
    return '{}: ogrzewanie wlaczone'.format(room)


def heaterOFF(gpionr, room):
    with open('/sys/class/gpio/gpio{}/value'.format(gpionr), 'w') as f:
        f.write("0")
    return '{}: ogrzewanie wlaczone'.format(room)


def heaterStatus(gpionr, room):
    with open('/sys/class/gpio/gpio{}/value'.format(gpionr)) as f:
        status = f.read()
    if status.split('\n')[0] == "1":
        return "{}: ogrzewanie jest wlaczone".format(room)
    if status.split('\n')[0] == "0":
        return "{}: ogrzewanie jest wylaczone".format(room)
    return "{}: status ogrzewania nieznany".format(room)


@app.route('/areyoualive')
def areyoualive():
    with open('{}/status'.format(webAPIRoot)) as f:
        return f.read().split('\n')[0]

@app.route('/lazienka-gora-on')
def lazienkaGoraOn():
    return heaterON(84, "lazienka-gora")
@app.route('/lazienka-gora-off')
def lazienkaGoraOff():
    return heaterOFF(84, "lazienka-gora")


@app.route('/gabinet-on')
def gabinetOn():
    return heaterON(82, "gabinet")
@app.route('/gabinet-off')
def gabinetOff():
    return heaterOFF(82, "gabinet")
@app.route('/gabinet-status')
def gabinetStatus():
    return heaterStatus(82, "gabinet")


@app.route('/sypialnia-on')
def sypialniaON():
    return heaterON(79, "sypialnia")
@app.route('/sypialnia-off')
def sypialniaOFF():
    return heaterOFF(79, "sypialnia")

@app.route('/przedpokoj-on')
def przepokojON():
    return heaterON(83, "przedpokoj")
@app.route('/przedpokoj-off')
def przedpokojOff():
    return heaterOFF(83, "przedpokoj")


@app.route('/lazienka-dol-on')
def lazienkaDolOn():
    return heaterON(87, "lazienka-dol")
@app.route('/lazienka-dol-off')
def lazienkaDolOff():
    return heaterOFF(87, "lazienka-dol")


@app.route('/zosia-on')
def zosiaON():
    return heaterON(80, "zosia")
@app.route('/zosia-off')
def zosiaOFF():
    return heaterOFF(80, "zosia")


@app.route('/justyna-on')
def justynaON():
    return heaterON(81, "justyna")
@app.route('/justyna-off')
def justynaOFF():
    return heaterOFF(81, "justyna")


@app.route('/salon-on')
def salonON():
    return heaterON(86, "salon")
@app.route('/salon-off')
def salonOFF():
    return heaterOFF(86, "salon")
@app.route('/salon-status')
def salonStatus():
    return heaterStatus(86, "salon")