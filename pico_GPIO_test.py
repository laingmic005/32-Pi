'''
Code written by Micah Laing on 2024-10-23 for the UVU Mechatronics 32 Pi project.
This program will test the GPIO outputs on the Raspberry Pico by blinking each LED
one by one. Enter 'Ctrl+C' in the terminal to stop the program.
'''
from machine import Pin
from utime import sleep

OBLED = Pin(25, Pin.OUT) # onboard LED

# define GIO pins 0 thru 15. Note that in the machine module the GPIO number is the same as the pin number
GPIO0 = Pin(0, Pin.OUT)
GPIO1 = Pin(1, Pin.OUT)
GPIO2 = Pin(2, Pin.OUT)
GPIO3 = Pin(3, Pin.OUT)
GPIO4 = Pin(4, Pin.OUT)
GPIO5 = Pin(5, Pin.OUT)
GPIO6 = Pin(6, Pin.OUT)
GPIO7 = Pin(7, Pin.OUT)
GPIO8 = Pin(8, Pin.OUT)
GPIO9 = Pin(9, Pin.OUT)
GPIO10 = Pin(10, Pin.OUT)
GPIO11 = Pin(11, Pin.OUT)
GPIO12 = Pin(12, Pin.OUT)
GPIO13 = Pin(13, Pin.OUT)
GPIO14 = Pin(14, Pin.OUT)
GPIO15 = Pin(15, Pin.OUT)

# this list will make operating all of our LEDs easier
GPIOlist = [OBLED, GPIO0, GPIO1, GPIO2, GPIO3, GPIO4, GPIO5, GPIO6, GPIO7, GPIO8, GPIO9, GPIO10, GPIO11, GPIO12, GPIO13, GPIO14, GPIO15]

print("LED starts flashing...")
while True:
    try:
        # each LED (including the onboard LED) will turn on and off one at a time
        for pin in GPIOlist:
            pin.toggle()
            sleep(0.2)
            pin.toggle()
            sleep(0.2)
    except KeyboardInterrupt:
        break

# Turn all the LEDs off when the program is cancelled
for pin in GPIOlist:
    pin.off()

print('Finished')
