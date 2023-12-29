# Setting up the Raspberry Pi

I opted to go with a Raspberry Pi 3 for initial development.

I gave up trying to get the internal WiFi to work and decided to use a WiFi dongle instead.

The WiFi dongle I used shows up under `lsusb` as:
```
Bus 001 Device 004: ID 148f:5370 Ralink Technology, Corp. RT5370 Wireless Adapter
```

## Use Rpi Images

I used the RPi Imager:
```
sudo apt install rpi-imager
```
and chose `Raspberry Pi OS (other)` and then `Raspberry Pi OS (Legacy, 32-bit) Lite` version.

## Set username and password

Under Rpi Imager's advanced settings, I configured it to use my username `dhylands` and my typical RPi password.

## Set the hostname

I also set the hostname to `wobble`.

## Initial WiFi setup

I set the Wifi to use my local SSID `Dream-Catcher` and entered the password. This wasn't quite enough
to get Wifi working (see additional steps below).

## Enable serial console

After flashing the image, I remounted the SDcard on my linux system and added the following to `/boot/config.txt`:
```
enable_uaet=1
enable_uaet=1
dtoverlay=pi3-disable-bt
dtoverlay=pi3-disable-wifi
```
This will enable the UART, and disable Bluetooth and WiFi.

I also edited `/boot/cmdline.txt` and removed `quiet` so I could see the kernel boot messages on the serial console.

## Edit Wifi Credentials

After booting (which takes a few minutes the first time), Wifi still wasn't working.

I editing the wpa_supplicant.conf file:
```
sudo vi /etc/wpa_supplicant/wpa_supplicant.conf
```
and added the line:
```
country=CA
```
and changed the psk to use the string version of my WiFi password.

The resulting wpa_supplicant.conf file looked like this:
```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
update_config=1
country=CA

network={
        ssid="Dream-Catcher"
        psk="***Enter WiFi Password here***"
}
```
and rebooted.

Now Wifi startedup automatically. I confirmed I could ssh into `wobble.local` and then did `ssh-copy-id wobble.local` to setup passwordless ssh.

## Update everything

```
sudo apt-get update
sudo apt-get upgrade
```

## Install Python

I added a 128x32 OLED from Adafruit, so I followed the instructions for installing it from:
https://learn.adafruit.com/circuitpython-on-raspberrypi-linux/installing-circuitpython-on-raspberry-pi
and


```
sudo apt-get install python3-pip
sudo apt install --upgrade python3-setuptools
pip3 install --upgrade adafruit-python-shell
wget https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/raspi-blinka.py
sudo -E env PATH=$PATH python3 raspi-blinka.py
```
Blinka rebooted after installing a bunch of stuff

I'm not currently using any SPI on the RPi, so I stopped here.

## Install 128x32 OLED from Adafruit

```
sudo power off
i2cdetect -y 1
```
Confirm device at 0x3c

```
sudo pip3 install adafruit-circuitpython-ssd1306
sudo apt-get install python3-pil
```

Downloaded the stats.py example and ran it (didn't need sudo).

I then edited /etc/rc.local
```
sudo vi /etc/rc.local
```
and added this line just befpre the `exit 0`
```
python3 /home/dhylands/stats.py &
```
