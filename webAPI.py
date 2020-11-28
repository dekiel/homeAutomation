from flask import Flask
app = Flask(__name__)



@app.route('/areyoualive')
def areyoualive():
    return "yes"
@app.route('/gabinet-on')
def gabinetOn():
    with open('/sys/class/gpio/gpio102/value', 'w') as f:
        f.write("1")
    return 'ogrzewanie w gabinecie wlaczone'
@app.route('/gabinet-off')
def gabinetOff():
    with open('/sys/class/gpio/gpio102/value', 'w') as f:
        f.write("0")
    return 'ogrzewanie w gabinecie wylaczone'
@app.route('/gabinet-status')
def gabinetStatus():
    with open('/sys/class/gpio/gpio102/value') as f:
        status = f.read()
    if status.split('\n')[0] == "1":
        return "ogrzewanie w gabinecie jest wlaczone"
    if status.split('\n')[0] == "0":
        return "ogrzewanie w gabinecie jest wylaczone"
    return "status ogrzewania w gabinecie nieznany"