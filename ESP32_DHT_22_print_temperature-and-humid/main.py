from machine import Pin
import time
import dht
from machine import SoftI2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd

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

# Display initial message
lcd.putstr("Hello")

h = -1
t = -1

while True:
    sensor.measure()  
    new_h = sensor.humidity()
    new_t = sensor.temperature()

    if h != new_h or t != new_t:
        h = new_h
        t = new_t
        lcd.clear()
        lcd.putstr("Hum: {}% Temp: {}C".format(h, t))

    if t > 40:
        led.on()
    else:
        led.off()

    time.sleep(1)
