#!/usr/bin/env python3
"""Shows CPU Information on the Adafruit 128x32 OLED display."""

# SPDX-FileCopyrightText: 2017 Tony DiCola for Adafruit Industries
# SPDX-FileCopyrightText: 2017 James DeVito for Adafruit Industries
# SPDX-License-Identifier: MIT

# This example is for use on (Linux) computers that are using CPython with
# Adafruit Blinka to support CircuitPython libraries. CircuitPython does
# not support PIL/pillow (python imaging library)!

import time
import signal
import subprocess

from board import SCL, SDA
import busio
from PIL import Image, ImageDraw, ImageFont
import adafruit_ssd1306

RUN = True
SPINNER = ('/', '-', '\\', '|')


def signal_handler(_signum, _frame):
    """Called when SIGNINT or SIGTERM is received."""
    global RUN  # pylint: disable=global-statement
    RUN = False


def main():
    """Main functions."""
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)

    # Create the I2C interface.
    i2c = busio.I2C(SCL, SDA)

    # Create the SSD1306 OLED class.
    # The first two parameters are the pixel width and pixel height.  Change these
    # to the right size for your display!
    disp = adafruit_ssd1306.SSD1306_I2C(128, 32, i2c)

    # Clear display.
    disp.fill(0)
    disp.show()

    # Create blank image for drawing.
    # Make sure to create image with mode '1' for 1-bit color.
    image = Image.new("1", (disp.width, disp.height))

    # Get drawing object to draw on image.
    draw = ImageDraw.Draw(image)

    # Draw a black filled box to clear the image.
    draw.rectangle((0, 0, disp.width, disp.height), outline=0, fill=0)

    # Draw some shapes.
    # First define some constants to allow easy resizing of shapes.
    padding = -2
    top = padding
    # Move left to right keeping track of the current x position for drawing shapes.
    left = 0

    # Load default font.
    font = ImageFont.load_default()

    # Alternatively load a TTF font.  Make sure the .ttf font file is in the
    # same directory as the python script!
    # Some other nice fonts to try: http://www.dafont.com/bitmap.php
    # font = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', 9)

    spin_idx = 0
    try:
        while RUN:
            # Draw a black filled box to clear the image.
            draw.rectangle((0, 0, disp.width, disp.height), outline=0, fill=0)

            # Shell scripts for system monitoring from here:
            # https://unix.stackexchange.com/questions/119126/command-to-display-memory-usage-disk-usage-and-cpu-load
            cmd = "hostname -I | cut -d' ' -f1"
            ip = subprocess.check_output(cmd, shell=True).decode("utf-8")
            cmd = 'cut -f 1 -d " " /proc/loadavg'
            cpu = subprocess.check_output(cmd, shell=True).decode("utf-8")
            cmd = "free -m | awk 'NR==2{printf \"Mem: %s/%s MB  %.2f%%\", $3,$2,$3*100/$2 }'"
            mem_usage = subprocess.check_output(cmd,
                                                shell=True).decode("utf-8")
            cmd = 'df -h | awk \'$NF=="/"{printf "Disk: %d/%d GB  %s", $3,$2,$5}\''
            disk = subprocess.check_output(cmd, shell=True).decode("utf-8")

            # Write four lines of text.
            draw.text((left, top + 0), "IP: " + ip, font=font, fill=255)
            draw.text((left, top + 8), "CPU load: " + cpu, font=font, fill=255)
            draw.text((left, top + 16), mem_usage, font=font, fill=255)
            draw.text((left, top + 25), disk, font=font, fill=255)

            draw.text((disp.width - 5, top), SPINNER[spin_idx], fill=255)

            spin_idx += 1
            spin_idx %= len(SPINNER)

            # Display image.
            disp.image(image)
            disp.show()
            time.sleep(0.1)
    except subprocess.CalledProcessError:
        pass

    # Clear the display
    print("Clearing...")
    disp.fill(0)
    disp.show()
    time.sleep(2)


if __name__ == "__main__":
    main()
