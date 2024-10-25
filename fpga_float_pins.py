'''
Code written by Micah Laing for the UVU Mechatronics 32 Pi project.
This program will generate a Verilog file to float all the FPGA pins 
so that they do not interfere with output from the Raspberry Pico
'''
from myhdl import block, instance, Signal, delay

@block
def main(led0, led1, led2, led3, led4, led5, led6, led7, led8, led9, led10, led11, led12, led13, led14, led15):
    @instance
    def logic():
        led0.next = None
        led1.next = None
        led3.next = None
        led2.next = None
        led4.next = None
        led5.next = None
        led6.next = None
        led7.next = None
        led8.next = None
        led9.next = None
        led10.next = None
        led11.next = None
        led12.next = None
        led13.next = None
        led14.next = None
        led15.next = None
        yield delay(10)  # Avoid an empty sensitivity list

    return logic

# Define signals for the LEDs
led0, led1, led2, led3, led4, led5, led6, led7, led8, led9, led10, led11, led12, led13, led14, led15 = [Signal(bool(0)) for _ in range(16)]

# Create and convert the LEDControl block to Verilog
main_function = main(led0, led1, led2, led3, led4, led5, led6, led7, led8, led9, led10, led11, led12, led13, led14, led15)
main_function.convert(hdl='Verilog', name='fpga_float_pins')
