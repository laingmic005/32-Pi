'''
The complete script to run on boot, which includes content from:

    - gpio_oled_display.py
    - detect-ssh-oled.py
'''
###### USER SET VALUES ######

font_path = "/home/mech/projects/display/UbuntuMono-R.ttf"
font_size = 17

boot_time = 20 # time delay before IP and hostname are retrieved
init_time = 10 # time hostanme and IP will be shown until login satus screen takes over

ssh_log_file = "/home/mech/active_ssh_sessions.log"
xrdp_log_file = "/var/log/xrdp.log"

###### DO NOT EDIT BELOW THIS LINE ######

# Import tools
import socket
import time
import smbus
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime

# load_fonts
font_r = ImageFont.truetype(font_path, font_size)
font_sm = ImageFont.truetype(font_path, font_size-3)
font_b = ImageFont.truetype(font_path, font_size+1)

I2C_ADDRESS = 0x3c # define the I2C address for OLED display

bus = smbus.SMBus(3) # create I2C bus. Use the correct SMBus number for your setup

# Function to initialilze the OLED display
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

# Function to get IP address
def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    ip_addr = s.getsockname()[0]
    s.close()
    return ip_addr

# Function to get hostname
def get_hostname():
    return socket.gethostname()

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

oled_init() # Initialize OLED
clear_oled() # Clear the display

welcome_msg = 'Retrieving data.\nPlease standby.' # Define welcome message to display on boot

###### BEGIN INITIALIZATION SEQUENCE ######
print('\nRetrieving IP address and hostname\n') # debug message

# Show welcome message in the center of screen
draw.text((0,20), welcome_msg, font = font_sm, fill = 1)
update_display()

# Show loading bar at the top
load_size = width // font_sm.getbbox('A')[2] # determine width of loading bar

for i in range(0, load_size-1):
    d_text = '/' * i
    draw.rectangle((0, 0, width, 22), outline=0, fill=0)  # Clear loading bar area
    draw.text((0, 0), f"[{d_text.ljust(load_size-2, ' ')}]", font=font_sm, fill=1)
    update_display()  # Update display with loading bar
    print(f"[{d_text.ljust(load_size-2, ' ')}]", end = '\r') # debug message

    if boot_time < 2:
        break
    time.sleep((boot_time) / (load_size + 2))

clear_oled() # clear the welcome message and loading bar
ip_addr = get_ip() # retrieve ip address
hostname = get_hostname() # retrieve hostname

# Draw IP address
draw.text((0,0), f"IP: {ip_addr}", font = font_r, fill = 1)
print(f'IP Address: {ip_addr}') # debug message

# Draw hostname
if font_r.getbbox('A')[2] * (len(hostname) + 5) <= width:
    draw.text((0, 20), f"HN: {hostname}", font=font_r, fill=1)
else:
    wrapped_hostname = wrap_text(hostname, width, font_r)
    draw.text((0, 20), f"HN: {wrapped_hostname}", font=font_r, fill=1)
print(f'Hostname: {hostname}\n') # debug message

update_display() # update display with IP and hostname

for i in range(init_time, -1, -1):
    print(f'{i}' + ' '*5, end = '\r') # debug message
    time.sleep(1)

###### LOGIN STATUS SEQUENCE ######

# Function to check for remote desktop user
def check_xrdp():
    with open(xrdp_log_file, 'r') as file:
        lines = file.readlines()
        if lines:
            latest_log = lines[-1].strip()

        if 'connected ok' in latest_log:
            return True
        else:
            return False
        
# Function to check for SSH user
def check_ssh():
    with open(ssh_log_file, 'r') as file:
        lines = file.readlines()
        if lines:
            latest_log = lines[-1].strip()

            if latest_log != '':
                return True
            else:
                return False


while True:
    # get the current time
    current_time = datetime.now().strftime("%H:%M:%S")

    # display remote connection status on OLED
    if check_xrdp() or check_ssh():
        draw.rectangle((0,0,width, height), outline = 0, fill = 0)
        draw.rectangle((0, 0, width, 15), outline = 1, fill = 1)
        draw.text((0,0), 'User Online', font = font_b, fill = 0)
        draw.text((0, 20), current_time, font = font_b, fill = 1)
        print('Remote user online - ' + current_time + ' '*80, end = '\r') # debug message
    else:
        draw.rectangle((0,0, width, height), outline = 0, fill = 0)
        # draw.rectangle((0, 0, 125, 15), outline = 1, fill = 0)
        draw.text((0,0), f'User Offline', font = font_b, fill = 1)
        draw.text((0, 20), current_time, font = font_b, fill = 1)
        print(f'No remote connections detected - {current_time}' + ' '*80, end = '\r') # debug message

    draw.text((0, 40), f'IP: {ip_addr}', font = font_sm, fill = 1) # display IP address

    update_display()
    time.sleep(1)
