## IMPORTS
import traceback
import queue
import sys
import time
import numpy as np
import settings
sys.path.append(settings.PYTHON_PACKAGES)
from TMC_2209.TMC_2209_StepperDriver import TMC_2209
import TMC_2209.TMC_2209_reg as reg


class Actuator():
    def __init__(self):
        self.motor = TMC_2209(settings.EN, settings.STEP, settings.DIR, baudrate=settings.TMC_BAUDRATE)
        self.y_offset = 0.95 * settings.RESOLUTION[1]
        self.x_offset = 0.5 * settings.RESOLUTION[0]
        self.theta_deg_offset = 87 # default: 90
        self.configure_motor()
        self.ref = 0
        self.error = 0
        self.ref_x = 0
        self.ref_y = 0
        self.mode = 0 # 0 is manual, 1 is auto
        self.manual_position = 0
        self.mcr_pos = 0
        self.pos = 0
        self.dir = 1
        # self.pos_queue = queue.Queue()
        # self.pos_queue.put(self.ref)


    def configure_motor(self):
        self.motor.set_current(settings.MAX_MOTORCURRENT)
        self.motor.set_interpolation(True)
        self.motor.set_microstepping_resolution(settings.MICROSTEP)
        self.motor.set_motor_enabled(True)
        self.motor.set_acceleration(settings.MAX_ACCELERATION)
        self.motor.set_max_speed(settings.MAX_SPEED)
        self.motor.set_vactual_rps(0)
        self.motor.readDRVSTATUS()
        self.motor.do_homing2(direction = -1, threshold = 8)


    def run(self, q, cond, shared_data):
        try:
            while True:
                if self.mode == 0:
                    self.move_to_pos_local(self.manual_position, margin=1)

                elif self.mode == 1:
                    # if new reference points exist: update reference
                    if not q.empty():
                        self.ref_y, self.ref_x = q.get()
                        self.convert_planar_to_angle()
                    self.error = self.ref-self.pos
                    self.move_to_pos_local(self.ref, margin=3)
                    # self.pos_queue.put(self.ref)
    
        except:
            traceback.print_exc()
            self.disable_motor()


    def move_to_pos(self):
        self.motor.run_to_position_steps(int(self.theta * settings.STEPRATIO))


    def disable_motor(self):
        self.motor.set_vactual_rps(0)
        self.motor.set_motor_enabled(False)


    def move_to_pos_local(self, deg, margin):
        # direction
        if deg > self.pos:
            self.dir = 1
            self.motor.set_direction_pin(1)
        if deg < self.pos:
            self.dir = 0
            self.motor.set_direction_pin(0)
        # steps
        if np.abs(self.pos - deg) > margin:
            self.motor.make_a_step()
            if self.dir == 1:
                self.mcr_pos += 1
            if self.dir == 0:
                self.mcr_pos -= 1
            self.pos = self.mcr_pos / settings.STEPRATIO
            time.sleep(1e-3) # controls the speed
    

    def convert_planar_to_angle(self):
        self.ref = np.round(np.rad2deg(np.arctan2((self.y_offset - self.ref_y),(self.ref_x - self.x_offset))), 4)
        # print(f'Motion detected at x = {self.ref_x - self.x_offset} and y = {self.y_offset - self.ref_y}, which is {self.ref} degrees')