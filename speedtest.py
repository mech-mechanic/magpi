import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess

# Raspberry Pi pin configuration:
RST = None     # on the PiOLED this pin isnt used
# Note the following are only used with SPI:
DC = 23
SPI_PORT = 0
SPI_DEVICE = 0

# Beaglebone Black pin configuration:
# RST = 'P9_12'
# Note the following are only used with SPI:
# DC = 'P9_15'
# SPI_PORT = 1
# SPI_DEVICE = 0

# 128x32 display with hardware I2C:
disp = Adafruit_SSD1306.SSD1306_128_32(rst=RST)

# Initialize library.
disp.begin()

# Clear display.
disp.clear()
disp.display()

# Create blank image for drawing.
# Make sure to create image with mode '1' for 1-bit color.
width = disp.width
height = disp.height
image = Image.new('1', (width, height))

# Get drawing object to draw on image.
draw = ImageDraw.Draw(image)

# Draw a black filled box to clear the image.
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Draw some shapes.
# First define some constants to allow easy resizing of shapes.
padding = -2
top = padding
bottom = height-padding
# Move left to right keeping track of the current x position for drawing shapes.
x = 0


# Load default font.
font = ImageFont.load_default()

# Alternatively load a TTF font.  Make sure the .ttf font file is in the same directory as the python script!
# Some other nice fonts to try: http://www.dafont.com/bitmap.php
# font = ImageFont.truetype('Minecraftia.ttf', 8)


# Draw a black filled box to clear the image
draw.rectangle((0,0,width,height), outline=0, fill=0)

# Begin speedtest code
from pyspeedtest import SpeedTest

test = SpeedTest()
host = test.host
ping = test.ping()
ping = format(ping, '.2f')
download = test.download()
upload = test.upload()
down = download/1000000
down = format(down, '.2f')
up = upload/1000000
up = format(up, '.2f')

host = host
ping = "Ping: " + ping + " ms"
down = "Download: " + down + " Mbps"
up = "Upload: " + up + " Mbps"


# Write four lines of text.
while True:
    draw.text((x, top), host,  font=font, fill=255)
    draw.text((x, top+8), ping, font=font, fill=255)
    draw.text((x, top+16), down,  font=font, fill=255)
    draw.text((x, top+25), up,  font=font, fill=255)

    # Display image.
    disp.image(image)
    disp.display()
    time.sleep(.1)
