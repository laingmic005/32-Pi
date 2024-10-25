'''
Code written by Micah Laing on 2024-10-23 for the UVU Mechatronics 32 Pi project.
This program will float all the pins on the Pico by changing them to inputs so that
the Pico will not interfere with the FPGA output.
'''
from machine import Pin
from utime import sleep

OBLED = Pin(25, Pin.OUT) # onboard LED

# set each pin to input. This will float the output
GPIO0 = Pin(0, Pin.IN)
GPIO1 = Pin(1, Pin.IN)
GPIO2 = Pin(2, Pin.IN)
GPIO3 = Pin(3, Pin.IN)
GPIO4 = Pin(4, Pin.IN)
GPIO5 = Pin(5, Pin.IN)
GPIO6 = Pin(6, Pin.IN)
GPIO7 = Pin(7, Pin.IN)
GPIO8 = Pin(8, Pin.IN)
GPIO9 = Pin(9, Pin.IN)
GPIO10 = Pin(10, Pin.IN)
GPIO11 = Pin(11, Pin.IN)
GPIO12 = Pin(12, Pin.IN)
GPIO13 = Pin(13, Pin.IN)
GPIO14 = Pin(14, Pin.IN)
GPIO15 = Pin(15, Pin.IN)
