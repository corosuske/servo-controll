#!/usr/bin/env python
from __future__ import division
from time import sleep
import serial
import os
import RPi.GPIO as GPIO
import curses
import time

# Import the PCA9685 module.
import Adafruit_PCA9685


GPIO.setmode(GPIO.BOARD)

# Uncomment to enable debug output.
#import logging
#logging.basicConfig(level=logging.DEBUG)

# Initialise the PCA9685 using the default address (0x40).
pwm = Adafruit_PCA9685.PCA9685()

# Alternatively specify a different address and/or bus:
#pwm = Adafruit_PCA9685.PCA9685(address=0x41, busnum=2)


# Configure min and max servo pulse lengths
servo_min = 150  # Min pulse length out of 4096
servo_max = 600  # Max pulse length out of 4096
# set the servo's staring points
servo1 = 350
servo2 = 450
servo3 = 250

LED = 7
# make sure the leds are truned off when the program starts
ledState = False

GPIO.setup(LED,GPIO.OUT)




def set_servo_pulse(channel, pulse):
    pulse_length = 1000000    # 1,000,000 us per second
    pulse_length //= 60       # 60 Hz
    print('{0}us per period'.format(pulse_length))
    pulse_length //= 4096     # 12 bits of resolution
    print('{0}us per bit'.format(pulse_length))
    pulse *= 1000
    pulse //= pulse_length
    pwm.set_pwm(channel, 0, pulse)

# Set frequency to 60hz, good for servos.
pwm.set_pwm_freq(60)





stdscr = curses.initscr()
curses.cbreak()
stdscr.keypad(1)
f = open("/tmp/pythonlog","w")
stdscr.addstr(0,10,"Hit 'z' to quit")
stdscr.refresh()

# loop read input and act accordingly

key = ''
try:
  while key != ord('z'):
      key = stdscr.getch()
      stdscr.addch(20,25,key)
      stdscr.refresh()
      if key == curses.KEY_UP: 
         #pwm.set_pwm(0, 0, servo_min)
         servo1 += 25
         if servo1 >= 476:
           servo1 = 475
         print (servo1)
      if key == curses.KEY_DOWN:
         #pwm.set_pwm(0, 0, servo_max)
         servo1 -= 25
         if servo1 <= 150:
           servo1 = 151
         print (servo1)

      if key == curses.KEY_LEFT:
         print ("left")
         servo2 += 25
         #pwm.set_pwm(1, 0, servo_min)
         if servo2 >= 600:
           servo2 = 599
      if key == curses.KEY_RIGHT:
         print ("right")
         servo2 -= 25
         #pwm.set_pwm(1, 0, servo_max)
         if servo2 <= 150:
           servo2 = 151
      if key == ord('c'):
         servo3 = 225
      if key == ord('v'):
         servo3 = 300
      if key == ord('l'):
         ledState = not ledState
         GPIO.output(LED, ledState)
      elif key == ord('f'):
          servo1 = 350
          servo2 = 350
          servo3 = 300
          print ("f")
      pwm.set_pwm(0, 0, servo1)
      pwm.set_pwm(1, 0, servo2)
      pwm.set_pwm(2, 0, servo3)
# cleanup 
# set all servos to center
finally:
  pwm.set_pwm(0, 0, 350)
  pwm.set_pwm(1, 0, 300)
  curses.endwin()
  GPIO.output(7, GPIO.LOW)
