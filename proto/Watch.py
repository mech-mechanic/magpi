import time

import Adafruit_GPIO.SPI as SPI
import Adafruit_SSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

import subprocess


class WatchFace:

  # Raspberry Pi pin configuration:
  RST = None     # on the PiOLED this pin isnt used
  # Note the following are only used with SPI:
  DC = 23
  SPI_PORT = 0
  SPI_DEVICE = 0

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

  def stats(self):
    count = 0

    while count < 100:
      # Draw a black filled box to clear the image.
      self.draw.rectangle((0,0,self.width,self.height), outline=0, fill=0)

      # Shell scripts for system monitoring from here : https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
      cmd = "hostname -I | cut -d\' \' -f1"
      IP = subprocess.check_output(cmd, shell = True )
      cmd = "top -bn1 | grep load | awk '{printf \"CPU Load: %.2f\", $(NF-2)}'"
      CPU = subprocess.check_output(cmd, shell = True )
      cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%sMB %.2f%%\", $3,$2,$3*100/$2 }'"
      MemUsage = subprocess.check_output(cmd, shell = True )
      cmd = "df -h | awk '$NF==\"/\"{printf \"Disk: %d/%dGB %s\", $3,$2,$5}'"
      Disk = subprocess.check_output(cmd, shell = True )

      # Write two lines of text.

      self.draw.text((self.x, self.top),       "IP: " + str(IP),  font=self.font, fill=255)
      self.draw.text((self.x, self.top+8),     str(CPU), font=self.font, fill=255)
      self.draw.text((self.x, self.top+16),    str(MemUsage),  font=self.font, fill=255)
      self.draw.text((self.x, self.top+25),    "Count: " + str(count),  font=self.font, fill=255)

      # Display image.
      self.disp.image(self.image)
      self.disp.display()
      time.sleep(.1)
      count = count + 1       

      return True


