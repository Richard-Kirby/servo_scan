#!/usr/bin/env python

# servo_demo.py
# 2016-10-07
# Public Domain

# servo_demo.py          # Send servo pulses to GPIO 4.
# servo_demo.py 23 24 25 # Send servo pulses to GPIO 23, 24, 25.

import sys
import time
import random
import pigpio

NUM_GPIO = 32

MIN_WIDTH = 500
MAX_WIDTH = 2000

step = [0] * NUM_GPIO
width = [0] * NUM_GPIO
used = [False] * NUM_GPIO

pi = pigpio.pi()

if not pi.connected:
    exit()

if len(sys.argv) == 1:
    G = [21]
else:
    G = []
    for a in sys.argv[1:]:
        G.append(int(a))

for g in G:
    used[g] = True
    step[g] = random.randrange(5, 25)
    if step[g] % 2 == 0:
        step[g] = -step[g]
    width[g] = random.randrange(MIN_WIDTH, MAX_WIDTH + 1)

print("Sending servos pulses to GPIO {}, control C to stop.".
      format(' '.join(str(g) for g in G)))

delay = 0.01

while True:

    try:
        #delay += 0.1

        print(delay)

        pi.set_servo_pulsewidth(21, 500)
        time.sleep(0.1)

        j= 500

        for i in range (500, 2275, 5):
            pi.set_servo_pulsewidth(21, i)
            time.sleep(delay)

            pi.set_servo_pulsewidth(25, 700)

            time.sleep(0.1)
            for j in range (700, 2500, 5):
                pi.set_servo_pulsewidth(25, j)
                print("i {} j{}".format(i, j))
                time.sleep(delay)

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

print("\nTidying up")

for g in G:
    pi.set_servo_pulsewidth(g, 0)

pi.stop()