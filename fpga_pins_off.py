'''
Code written by Micah Laing on 2024-10-23 for the UVU Mechatronics 32 Pi project.
This program will generate a Verilog file that will pull down the FPGA pins.
'''
from myhdl import block, instance, Signal, delay

@block
def main(led0, led1, led2, led3, led4, led5, led6, led7, led8, led9, led10, led11, led12, led13, led14, led15):
    @instance
    def logic():
        led0.next = 0
        led1.next = 0
        led2.next = 0
        led3.next = 0
        led4.next = 0
        led5.next = 0
        led6.next = 0
        led7.next = 0
        led8.next = 0
        led9.next = 0
        led10.next = 0
        led11.next = 0
        led12.next = 0
        led13.next = 0
        led14.next = 0
        led15.next = 0
        yield delay(10)  # Avoid an empty sensitivity list

    return logic

# Define signals for the LEDs
led0, led1, led2, led3, led4, led5, led6, led7, led8, led9, led10, led11, led12, led13, led14, led15 = [Signal(bool(0)) for _ in range(16)]

# Create and convert the LEDControl block to Verilog
main_function = main(led0, led1, led2, led3, led4, led5, led6, led7, led8, led9, led10, led11, led12, led13, led14, led15)
main_function.convert(hdl='Verilog', name='fpga_pins_off')
