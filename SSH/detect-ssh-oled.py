'''
Code written by Micah Laing on 8 January 2025. This program will detect if a user is
connected via SSH to the RPi-5 this code is running on and display the status on an
external OLED via GPIO pins 17 & 27. You must be running the shell script that writes
the status of SSH sessions to a log file.
'''

import socket
import time
import smbus
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# User set values
font_path = "/home/mech/projects/display/UbuntuMono-R.ttf"
font_size = 18

log_file = '/home/mech/active_ssh_sessions.log'

# Define the I2C address for the OLED display
I2C_ADDRESS = 0x3C

# Create I2C bus
bus = smbus.SMBus(3)  # Use the correct SMBus number for your setup

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

# Function to clear the display
def clear_oled():
    # Clear each of the 8 pages for the 64 pixels height
    for page in range(8):  # There are 8 pages for a 64-pixel height display
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
    update_display()  # Update display after clearing

# Create blank image for drawing
width = 128
height = 64
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

# Load fonts
font_m = ImageFont.truetype(font_path, font_size)

# Function to update the display with the image
def update_display():
    # Convert image to 1-bit pixels
    disp_image = image.convert('1')
    
    # Prepare byte array to send to display
    byte_array = []
    for i in range(0, height, 8):  # Each byte represents 8 vertical pixels
        for j in range(width):
            byte = 0
            for bit in range(8):
                if i + bit < height and disp_image.getpixel((j, i + bit)) == 1:
                    byte |= (1 << bit)  # Set bit if pixel is set
            byte_array.append(byte)
    
    # Write the buffer in chunks
    write_buffer_in_chunks(byte_array)

# Function to write the display buffer in chunks
def write_buffer_in_chunks(buffer):
    for start in range(0, len(buffer), 32):
        chunk = buffer[start:start + 32]
        if chunk:  # Ensure chunk is not empty
            bus.write_i2c_block_data(I2C_ADDRESS, 0x40, chunk)

# Function to wrap text
def wrap_text(text, screen_width, font):
    size = font.getbbox('A')[2]
    max_chars = screen_width // (size)-5
    characters = [char for char in text]
    new_chars = []
    for i in range(max_chars):
        new_chars.append(characters[i])
    new_chars.append('-\n       ')
    for j in range(max_chars, len(characters), 1):
        new_chars.append(characters[j])
    return ''.join(new_chars)

# Initialize OLED
oled_init()

# Clear the display
clear_oled()

load_size = width // font_m.getbbox('A')[2]

# Main loop

while True:
    # retrieve latest message from SSH log file
    with open(log_file, 'r') as file:
        log_message = file.read().split('\n')
    try:
        log_message = log_message[-2]
    except IndexError:
        log_message = log_message[-1]

    # get the current time
    current_time = datetime.now().strftime("%H:%M:%S")

    # display SSH connection status on OLED
    if log_message != '':
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((0, 0), 'SSH Connected', font=font_m, fill=1)
        draw.text((0,20), current_time, font = font_m, fill = 1)
        print(log_message + ' '*80, end = '\r')
    else:
        draw.rectangle((0, 0, width, height), outline=0, fill=0)
        draw.text((0,0), f'User Offline', font = font_m, fill = 1)
        draw.text((0,20), current_time, font = font_m, fill = 1)
        print(f'No SSH connections detected - {current_time}' + ' '*80, end = '\r')

    update_display()
    time.sleep(1)

