#!/usr/bin/env python

# servo_demo.py
# 2016-10-07
# Public Domain

# servo_demo.py          # Send servo pulses to GPIO 4.
# servo_demo.py 23 24 25 # Send servo pulses to GPIO 23, 24, 25.

import time
import numpy

import pigpio

pi = pigpio.pi()

if not pi.connected:
    exit()

class PanTiltController:
    def __init__(self, pan_start, pan_end, pan_gpio, tilt_start, tilt_end, tilt_gpio):
        self.pan_start = pan_start
        self.pan_end = pan_end
        self.pan_gpio = pan_gpio

        self.tilt_start = tilt_start
        self.tilt_end = tilt_end
        self.tilt_gpio = tilt_gpio

    def pan_tilt(self, pan_begin, pan_stop, steps, delay):
        pan_array = numpy.linspace(int(pan_begin * (self.pan_end - self.pan_start) + self.pan_start),
                                   int(pan_stop * (self.pan_end - self.pan_start) + self.pan_start), steps, 'int16')

        delay_array = [delay] * steps

        cmd_array = list(zip(pan_array, delay_array))

        print(cmd_array)

        #print(pan_array)

delay = 0.01

pan_tilt_controller = PanTiltController(700, 2400, 25, 500, 2400, 21)

pan_tilt_controller.pan_tilt(0, 1, 50, 0.01)

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

        '''
        print("S2 - mid")
        pi.set_servo_pulsewidth(25, 1500)
        time.sleep(delay)
        print("S2 - low")
        pi.set_servo_pulsewidth(25, 500)
        time.sleep(delay)
        print("S2 - high")
        pi.set_servo_pulsewidth(25, 2500)
        time.sleep(delay)
        '''

        #pi.set_servo_pulsewidth(21, 1500)
        #time.sleep(delay)
        #pi.set_servo_pulsewidth(21, 1000)
        #time.sleep(delay)
        #pi.set_servo_pulsewidth(21, 2000)
        #time.sleep(delay)
        #pi.set_servo_pulsewidth(21, 1000)
        #time.sleep(delay)

        '''
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
        break

    except:
        raise()

    finally:
        print("\nTidying up")
        pi.stop()