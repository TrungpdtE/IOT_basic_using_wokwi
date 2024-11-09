import time
import dht
from machine import Pin, SoftI2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd


TRIGGER_PIN = 15
ECHO_PIN = 0
BUZZER_PIN = 2


trigger = Pin(TRIGGER_PIN, Pin.OUT)
echo = Pin(ECHO_PIN, Pin.IN)
buzzer = Pin(BUZZER_PIN, Pin.OUT)
sensor = dht.DHT22(Pin(14))
i2c_addr = 0x27
totalRows = 2
totalColumns = 16
i2c = SoftI2C(scl=Pin(23), sda=Pin(21), freq=10000)
lcd = I2cLcd(i2c, i2c_addr, totalRows, totalColumns)
lcd.putstr("Hello")
h = -1

def produce_sound():
    buzzer.value(1)
    time.sleep(0.1)
    buzzer.value(0)

def get_distance():
    trigger.value(0)
    time.sleep(0.000002)
    trigger.value(1)
    time.sleep(0.00001)
    trigger.value(0)

    timeout = time.ticks_ms() + 100
    start_time = time.ticks_us()
    while echo.value() == 0:
        start_time = time.ticks_us()
        if time.ticks_ms() > timeout:
            print("Echo not received!")
            return -1

    timeout = time.ticks_ms() + 100
    while echo.value() == 1:
        end_time = time.ticks_us()
        if time.ticks_ms() > timeout:
            print("Echo signal too long!")
            return -1

    duration = time.ticks_diff(end_time, start_time)
    distance = duration * 0.0343 / 2
    return distance

while True:
    distance = get_distance()
    if distance >= 0:
        print(f"Distance: {distance:.2f} cm")
        time.sleep(0.001)
        lcd.clear()
        lcd.putstr("Distance:       ")
        lcd.putstr(str(distance))

        if distance < 50:
            produce_sound()

    time.sleep(2)