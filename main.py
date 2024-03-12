#!/usr/bin/env python3

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
socketio = SocketIO(app, ping_timeout=60, ping_interval=25)

updated_movement = False
cond = threading.Condition()

def main():
    detector_thread = threading.Thread(target=detector.run, args=(cond, updated_movement,))
    actuator_thread = threading.Thread(target=actuator.run, args=(detector.q, cond, updated_movement,))
    app_thread = threading.Thread(target=run_socketio)
    # info_thread = threading.Thread(target=emit_info) #, args=(actuator.pos_queue,))

    app_thread.start()
    detector_thread.start()
    actuator_thread.start()
    # info_thread.start()

    detector_thread.join()
    actuator_thread.join()
    app_thread.join()
    # info_thread.join()

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('update_power')
def update_power(data):
    powerlevel = int(data['value'])
    heater.set_power(powerlevel)
    emit('power_updated', {'value': str(powerlevel)}, broadcast=True)   

@socketio.on('update_position')
def update_position(data):
    manual_position = int(data['value'])
    actuator.manual_position = manual_position # in degrees
    emit('position_updated', {'value': str(manual_position)}, broadcast=True)   

@socketio.on('select-mode')
def select_mode(data):
    actuator.mode = int(data['value'])
    emit('mode-updated', {'value': str(actuator.mode)}, broadcast=True)

def init_values():
    emit('mode-updated', {'value': str(actuator.mode)}, broadcast=True)
    emit('power_updated', {'value': str(heater.powerlevel)}, broadcast=True)
    emit('position_updated', {'value': str(int(actuator.manual_position))}, broadcast=True)     

def run_socketio():
    socketio.run(app, host='0.0.0.0', port=5000) #, debug=False, use_reloader=False, log_output=False)
    print('init values')
    init_values()

# def emit_info(): #(pos_queue):
#     while True: 
#         actuator_pos = int(actuator.pos_queue.get())
#         # heater_info = heater.pow_queue
#         socketio.emit('position_updated', {'value': str(actuator_pos)})   


if __name__ == '__main__':
    main()
