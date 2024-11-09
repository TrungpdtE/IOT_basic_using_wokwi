# main.py
from machine import Pin
import time
import dht
import network
import wifi
from machine import SoftI2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
import ifttt  # Nhập tệp ifttt.py

# Initialize LED
led = Pin(5, Pin.OUT)

# Initialize DHT22 sensor
sensor = dht.DHT22(Pin(14))

# I2C configuration
I2C_ADDR = 0x27
totalRows = 2
totalColumns = 16
i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=100000)

# Initialize LCD
lcd = I2cLcd(i2c, I2C_ADDR, totalRows, totalColumns)

# Connect to WiFi
def connect_internet():
    print("Connecting to WiFi", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(wifi.ssid, wifi.password)
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.1)
    print(" Connected!")
    print("IP Address:", sta_if.ifconfig()[0])  

# Main loop
entry_count = 0  # Initialize entry counter
connect_internet()  # Connect to WiFi

while True:
    sensor.measure()  
    new_h = sensor.humidity()
    new_t = sensor.temperature()

    # Update LCD display
    lcd.clear()
    lcd.putstr("Hum: {}% Temp: {}C".format(new_h, new_t))

    # Check for motion (assuming motion sensor is connected to another pin)
    motion_sensor = Pin(12, Pin.IN)
    motion_detected = motion_sensor.value()

    if motion_detected == 1:
        led.on()
        entry_count += 1  # Increment the entry count
        print("Motion detected! Entry count:", entry_count)
        ifttt.alert_entry_count(entry_count)  # Log entry to Google Sheets
    else:
        led.off()

    # Delay for stability
    time.sleep(5)  # Increase sleep time to reduce request frequency
