## IMPORTS
import sys
import time
import numpy as np
sys.path.append('/home/pi/.local/lib/python3.7/site-packages')
from TMC_2209.TMC_2209_StepperDriver import TMC_2209
import TMC_2209.TMC_2209_reg as reg
import settings


class Actuator():
    def __init__(self):
        self.motor = TMC_2209(settings.EN, settings.STEP, settings.DIR, baudrate=settings.TMC_BAUDRATE)
        self.theta_deg = 0
        self.y_offset = 0.95 * settings.RESOLUTION[1]
        self.x_offset = 0.5 * settings.RESOLUTION[0]
        self.theta_deg_offset = 90
        self.configure_motor()

    def configure_motor(self):
        self.motor.set_current(settings.MAX_MOTORCURRENT)
        self.motor.set_interpolation(True)
        self.motor.set_microstepping_resolution(settings.MICROSTEP)
        self.motor.set_motor_enabled(True)
        self.motor.set_acceleration(settings.MAX_ACCELERATION)
        self.motor.set_max_speed(settings.MAX_SPEED)
        self.motor.do_homing2(direction = -1, threshold = 8)

    
    def run(self, q):
        try:
            while True:
                if not q.empty():
                    y, x = q.get()
                    self.theta_deg = np.round(np.rad2deg(np.arctan2((self.y_offset - y),(x - self.x_offset))), 3)
                    print(f'Motion detected at x = {x - self.x_offset} and y = {self.y_offset - y}, which is {self.theta_deg} degrees')
                    self.move()
        except Exception as e:
            print(e)
            self.disable_motor()

    def move(self):
        self.motor.run_to_position_steps(int(self.theta_deg * settings.STEPRATIO))

    def disable_motor(self):
        self.motor.set_motor_enabled(False)

    def custom_vel_path(self):
        v = -1500
        print(self.motor.get_current_position())
        self.motor.tmc_uart.write_reg_check(reg.VACTUAL, round(v))
        time.sleep(0.5)
        v = 0
        self.motor.tmc_uart.write_reg_check(reg.VACTUAL, round(v))
        print(self.motor.get_current_position())
        # self.motor.set_vactual(vactual=0)
        