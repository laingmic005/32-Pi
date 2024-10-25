'''
Code written by Micah Laing on 2024-10-23 for the UVU Mechatronics 32 Pi project. This program
will set the GPIO pins on the Pico to read the output from the FPGA, and interpret the output as a Binary
number. The program will then convert and display that number in binary, decimal, and hexidecimal.

Note that I have GPIO15 as the least significant digit. If you would prefer GPIO0 be least significant,
reverse the order of GPIOlist
'''
from machine import Pin
from utime import sleep

OBLED = Pin(25, Pin.OUT) # onboard LED

# define GPIO pins 0 thru 15. Note that in the machine module the GPIO number is the same as the pin number
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

# this list will make operating on all of our LEDs easier
GPIOlist = [GPIO0, GPIO1, GPIO2, GPIO3, GPIO4, GPIO5, GPIO6, GPIO7, GPIO8, GPIO9, GPIO10, GPIO11, GPIO12, GPIO13, GPIO14, GPIO15]

# read the value of each LED and add it to pinvalues list. GPIO15 is the least significant digit. To make GPIO0 least significant, reverse the order of GPIOlist
pinvalues = []
for pin in GPIOlist:
    pinvalues.append(pin.value())

# convert pinvalues list to a single binary number string
binary_string = ''.join(map(str, pinvalues))

# convert binary number to decimal
integer_value = int(binary_string, 2)

# convert decimal number to hexidecimal
hex_value = hex(integer_value)

# display values in terminal
print(f'Binary:\t\t{binary_string}\nDecimal:\t{integer_value}\nHex:\t\t{hex_value}')
