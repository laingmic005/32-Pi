# Code written by Micah Laing on 2024-11-1 for the UVU Mechatronics Lab 32-Pi project.
# This is a driver that will initialize an OLED display from GPIO pins 17 and 27 on RPi-5.

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
display_text("Initializing")
