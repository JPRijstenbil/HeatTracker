from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import threading

from actuator import Actuator
from motion_detector import MotionDetector
from heater import Heater

detector = MotionDetector()
heater = Heater()
actuator = Actuator()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

powerlevel = 0

def main():

    actuator.custom_vel_path()
    # detector_thread = threading.Thread(target=detector.run)
    # actuator_thread = threading.Thread(target=actuator.run, args=(detector.q,))
    # app_thread = threading.Thread(target=run_socketio)

    # app_thread.start()
    # detector_thread.start()
    # actuator_thread.start()

    # detector_thread.join()
    # actuator_thread.join()
    # app_thread.join()


@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('update_power')
def update_power(data):
    powerlevel = int(data['value'])
    heater.set_power(powerlevel)
    emit('power_updated', {'value': str(powerlevel)}, broadcast=True)   

def run_socketio():
    socketio.run(app, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()