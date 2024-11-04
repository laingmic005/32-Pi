'''
Code written by Micah Laing on 04 November 2024 for the UVU Mechatronics
Lab 32-pi project. This code will read output from FPGA and interpret it
as a binary value from the RPi-5. It will then display the binary, integer,
and hex value of that number on the OLED screen.
'''

from gpiozero import Button
import time

# Define GPIO pins
GPIO_PINS = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]  # Adjust as needed

# Set up each pin as a Button (input)
buttons = [Button(pin) for pin in GPIO_PINS]

# Read the value of each pin and store it in a list
pin_values = [button.is_pressed for button in buttons]

# invert pin values
inverted_values = []
for value in pin_values:
    if value == 0:
        inverted_values.append(1)
    else:
        inverted_values.append(0)

# Convert the list of pin values to a binary string
binary_string = ''.join(map(str, map(int, inverted_values)))

# Convert binary string to decimal
integer_value = int(binary_string, 2)

# Convert decimal value to hexadecimal
hex_value = hex(integer_value)

# Display values in terminal
print(f'Binary:\t\t{binary_string}\nDecimal:\t{integer_value}\nHex:\t\t{hex_value}')

import smbus
import time
from PIL import Image, ImageDraw, ImageFont

# OLED I2C address
I2C_ADDRESS = 0x3C
I2C_BUS_NUMBER = 3  # Use the software-configured I2C bus on GPIO 17 and 27

# Screen width and height
SCREEN_WIDTH = 128
SCREEN_HEIGHT = 64

# Create an instance of the I2C bus
bus = smbus.SMBus(I2C_BUS_NUMBER)

# Function to initialize the OLED display
def oled_init():
    commands = [
        0xAE,  # Display off
        0xD5, 0x80,  # Set display clock divide ratio/oscillator frequency
        0xA8, 0x3F,  # Set multiplex ratio (1 to 64)
        0xD3, 0x00,  # Set display offset
        0x40,        # Set start line address
        0x8D, 0x14,  # Enable charge pump regulator
        0x20, 0x00,  # Set memory addressing mode to horizontal
        0xA1,        # Set segment re-map 0 to 127
        0xC8,        # Set COM output scan direction
        0xDA, 0x12,  # Set COM pins hardware configuration
        0x81, 0x7F,  # Set contrast control
        0xD9, 0xF1,  # Set pre-charge period
        0xDB, 0x40,  # Set VCOMH deselect level
        0xA4,        # Enable display RAM content
        0xA6,        # Set normal display mode
        0xAF         # Display on
    ]
    
    # Send each command to the OLED
    for cmd in commands:
        bus.write_byte_data(I2C_ADDRESS, 0x00, cmd)
        time.sleep(0.01)  # Small delay to ensure command processing

# Function to clear the OLED display
def clear_display():
    # Loop through each page (8 pages for a 64-pixel height display)
    for page in range(8):
        # Set the page address and column start address
        bus.write_i2c_block_data(I2C_ADDRESS, 0x00, [0xB0 + page, 0x00, 0x10])

        # Send 128 bytes of 0 in chunks of 32 bytes
        empty_row = [0x00] * SCREEN_WIDTH
        for i in range(0, SCREEN_WIDTH, 32):
            chunk = empty_row[i:i + 32]
            bus.write_i2c_block_data(I2C_ADDRESS, 0x40, chunk)

# Function to draw text on the display
def display_text(text, font_path="conthrax-sb.otf", font_size=12):
    # Load font and create a blank image
    font = ImageFont.load_default()
    image = Image.new("1", (SCREEN_WIDTH, SCREEN_HEIGHT))
    draw = ImageDraw.Draw(image)

    # Draw the text
    draw.text((0, 0), text, font=font, fill=1)

    # Send the image data to the OLED
    update_display(image)

# Function to update the OLED display with an image
def update_display(image):
    # Convert image to 1-bit pixels
    disp_image = image.convert('1')

    # Prepare byte data to send to display
    byte_data = []
    for i in range(0, SCREEN_HEIGHT, 8):  # Each byte represents 8 vertical pixels
        for j in range(SCREEN_WIDTH):
            byte = 0
            for bit in range(8):
                if i + bit < SCREEN_HEIGHT and disp_image.getpixel((j, i + bit)) == 1:
                    byte |= (1 << bit)  # Set bit if pixel is set
            byte_data.append(byte)
    
    # Write the buffer in chunks of 32 bytes
    for i in range(0, len(byte_data), 32):
        chunk = byte_data[i:i + 32]
        bus.write_i2c_block_data(I2C_ADDRESS, 0x40, chunk)

# Run initialization and test display
oled_init()
clear_display()
display_text(f'Binary:\n{binary_string}\nDecimal: {integer_value}\nHex: {hex_value}')

