#!/usr/bin/env python

# servo_demo.py
# 2016-10-07
# Public Domain

# servo_demo.py          # Send servo pulses to GPIO 4.
# servo_demo.py 23 24 25 # Send servo pulses to GPIO 23, 24, 25.

import board
import busio
import time
import numpy as np
import sys

import pigpio
import adafruit_vl53l0x

# Initialize I2C bus and sensor.
# Optionally adjust the measurement timing budget to change speed and accuracy.
# See the example here for more details:
#   https://github.com/pololu/vl53l0x-arduino/blob/master/examples/Single/Single.ino
# For example a higher speed but less accurate timing budget of 20ms:
# vl53.measurement_timing_budget = 20000
# Or a slower but more accurate timing budget of 200ms:
# vl53.measurement_timing_budget = 200000
# The default timing budget is 33ms, a good compromise of speed and accuracy.

# Lidar set up.

i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)



pi = pigpio.pi()

if not pi.connected:
    exit()

class PanTiltController:
    def __init__(self, pan_start, pan_end, pan_gpio, tilt_start, tilt_end, tilt_gpio, first_move_delay):
        self.pan_start = pan_start
        self.pan_end = pan_end
        self.pan_gpio = pan_gpio

        self.tilt_start = tilt_start
        self.tilt_end = tilt_end
        self.tilt_gpio = tilt_gpio
        self.first_move_delay = first_move_delay

    # 
    def pan_tilt(self, pan_begin, pan_stop, pan_steps, pan_delay):
        pan_array = np.linspace(int(pan_begin * (self.pan_end - self.pan_start) + self.pan_start),
                                   int(pan_stop * (self.pan_end - self.pan_start) + self.pan_start), pan_steps,
                                   dtype = np.int16)

        delay_array = [pan_delay] * pan_steps

        pan_cmd_array = list(zip(pan_array, delay_array))

        print(pan_cmd_array)

        # Need a longer delay for first move - might have to move further.
        first_move = True

        for pan_move in pan_cmd_array:
            print(pan_move)
            pi.set_servo_pulsewidth(self.pan_gpio, int(pan_move[0]))
            if first_move:
                first_move = False
                time.sleep(self.first_move_delay)

            time.sleep(pan_move[1])



        #print(pan_array)

try:

    pan_tilt_controller = PanTiltController(500, 2300, 21, 660, 2500, 25, 2)

    pan_tilt_controller.pan_tilt(0, 1, 50, 0.01)
    pan_tilt_controller.pan_tilt(1, 0, 50, 0.01)

    while True:

            print('Range: {0}mm'.format(vl53.range))
            time.sleep(.1)

            if vl53.range < 100:
                pan_tilt_controller.pan_tilt(0, 1, 50, 0.01)
                pan_tilt_controller.pan_tilt(1, 0, 50, 0.01)

    '''
    
    while True:
    
        try:
            #delay += 0.1
    
            print(delay)
    
            pi.set_servo_pulsewidth(21, 500)
            time.sleep(0.1)
    
    
    
            j= 500
    
            step = 100
            step_normal_dir = True
    
            for i in range (500, 2400, step):
                pi.set_servo_pulsewidth(21, i)
                time.sleep(delay)
    
                #pi.set_servo_pulsewidth(25, 700)
    
                time.sleep(2)
    
                if step_normal_dir == True:
                    for j in range (700, 2500, step):
                        pi.set_servo_pulsewidth(25, j)
                        print("dir {} i {} j{}".format(step_normal_dir, i, j))
                        time.sleep(delay)
                else:
                    for j in range (2500, 699, -step):
                        pi.set_servo_pulsewidth(25, j)
                        print("dir {} i {} j{}".format(step_normal_dir, i, j))
                        time.sleep(delay)
                step_normal_dir ^= True
    
                time.sleep(0.1)
    
            print("S2 - mid")
            pi.set_servo_pulsewidth(25, 1500)
            time.sleep(delay)
            print("S2 - low")
            pi.set_servo_pulsewidth(25, 500)
            time.sleep(delay)
            print("S2 - high")
            pi.set_servo_pulsewidth(25, 2500)
            time.sleep(delay)
    
            #pi.set_servo_pulsewidth(21, 1500)
            #time.sleep(delay)
            #pi.set_servo_pulsewidth(21, 1000)
            #time.sleep(delay)
            #pi.set_servo_pulsewidth(21, 2000)
            #time.sleep(delay)
            #pi.set_servo_pulsewidth(21, 1000)
            #time.sleep(delay)
    
            for g in G:
    
                pi.set_servo_pulsewidth(g, width[g])
    
                # print(g, width[g])
    
                width[g] += step[g]
    
                if width[g] < MIN_WIDTH or width[g] > MAX_WIDTH:
                    step[g] = -step[g]
                    width[g] += step[g]
    
            time.sleep(0.1)
    '''

except KeyboardInterrupt:
    print("Quitting the program due to Ctrl-C")

except:
    print("Unexpected error:", sys.exc_info()[0])
    raise

finally:
    print("\nTidying up")
    pi.stop()