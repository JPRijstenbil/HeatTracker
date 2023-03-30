import RPi.GPIO as GPIO
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

GPIO.setmode(GPIO.BOARD)
GPIO.setup(13, GPIO.OUT)

nervousness = 5
power = 1300

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('toggle_gpio')
def toggle_gpio():
    pin_state = GPIO.input(13)
    GPIO.output(13, not pin_state)
    emit('gpio_toggled', {'state': not pin_state}, broadcast=True)

@socketio.on('update_nervousness')
def update_nervousness(data):
    global nervousness
    nervousness = int(data['value'])
    emit('nervousness_updated', {'value': nervousness}, broadcast=True)

@socketio.on('update_power')
def update_power(data):
    global power
    power = int(data['value']) * 700 + 600
    emit('power_updated', {'value': power}, broadcast=True)

if __name__ == '__main__':
    try:
        socketio.run(app, host='0.0.0.0', port=5000)
    finally:
        GPIO.cleanup()