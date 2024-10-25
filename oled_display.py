'''
Code written by Micah Laing on October 4, 2024 for the Mauna Kea
(32 Pi) Project.

Acknowledgements: Zachary Pittman, for providing the template
code which this code was based on.
'''

# User set values
font_file_name = 'conthrax-sb.otf'
font_size = 14
boot_time = 30
display_time = 30

import socket
import time
from PIL import Image, ImageDraw, ImageFont
import Adafruit_GPIO.I2C as I2C
import Adafruit_SSD1306
import Adafruit_GPIO.Platform as Platform
Platform.platform_detect = lambda: Platform.RASPBERRY_PI

# Define the I2C address and the reset pin
I2C_ADDRESS = 0x3C
RST = None

# Initialize the display
disp = Adafruit_SSD1306.SSD1306_128_64(rst=RST, i2c_address=I2C_ADDRESS)
disp.begin()
disp.clear()
disp.display()

# Create blank image for drawing
width = disp.width
height = disp.height
image = Image.new('1', (width, height))
draw = ImageDraw.Draw(image)

# load fonts
font_path = f"/home/mech/projects/display/{font_file_name}"
font = ImageFont.truetype(font_path, font_size)
font_sm = ImageFont.truetype(font_path, font_size-2)
_font_mono_path = "/home/mech/projects/display/UbuntuMono-R.ttf"
font_mono = ImageFont.truetype(_font_mono_path, 11)
font_mono_lg = ImageFont.truetype(_font_mono_path, 14)

# function to get IP address
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_addr = s.getsockname()[0]
    s.close()
    return ip_addr

# function to get hostname
def get_hostname():
    return socket.gethostname()

# function to wrap text
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

# function to clear display
def clear_oled():
    disp.clear()
    disp.display()
    draw.rectangle((0, 0, width, height), outline=0, fill=0)
    return None

# define welcome message
welcome_msg = 'Retrieving data.\nPlease standby.'
load_size = width//font_mono.getbbox('A')[2]

# clear the image
clear_oled()

# main loop
while True:

    # show welcome message
    draw.text((0, 20), welcome_msg, font = font_sm, fill = 255)
    disp.image(image)
    disp.display()

    # show loading bar etm
    for i in range(0, load_size+1, 1):
        d_text = '/'*i
        draw.text((0, 0), f"[{d_text.ljust(load_size, ' ')}]", font = font_mono, fill = 255)
        disp.image(image)
        disp.display()
        draw.rectangle((0, 0, width, 22), outline=0, fill=0)
        if boot_time < 2:
            break
        time.sleep((boot_time)/(load_size+2))

    # clear welcome message
    clear_oled()

    # get IP address and hostname
    ip_addr = get_ip()
    hostname = get_hostname()

    # draw IP address in yellow
    draw.text((0, 0), f"IP: {ip_addr}", font=font, fill=255)

    # draw hostname in blue
    if font.getbbox('A')[2]*(len(hostname)+5) <= width:
        draw.text((0, 20), f"HN: {hostname}", font=font, fill=255)
    else:
        wrapped_hostname = wrap_text(hostname, width, font)
        draw.text((0, 20), f"HN: {wrapped_hostname}", font=font, fill=255)
        
    # display IP and hostname
    disp.image(image)
    disp.display()

    # display the time remaining until screen turns off
    for i in range(display_time, -1, -1):
        draw.text((0, 45), f"{i}", font = font_sm, fill = 255)
        disp.image(image)
        disp.display()
        time.sleep(1)
        draw.rectangle((0, 45, 20, 75), outline=0, fill=0)

    # clear screen and break loop
    clear_oled()
    break
