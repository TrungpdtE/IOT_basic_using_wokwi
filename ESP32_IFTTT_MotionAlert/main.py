from machine import Pin
import time
import ifttt
import network
import wifi

led_pin = 14
sensor_pin = 12
led = Pin(led_pin, Pin.OUT)
sensor = Pin(sensor_pin, Pin.IN)
def connect_internet():
  print("Connecting to WiFi", end="")
  sta_if = network.WLAN(network.STA_IF)
  sta_if.active(True)
  sta_if.connect(wifi.ssid, wifi.password)
  while not sta_if.isconnected():
    print(".", end="")
    time.sleep(0.1)
  print(" Connected!")

def loop():
  while True:
    value = sensor.value()
    print(value)
    if(value == 1):
      led.on()
      
      ifttt.alert_motion(value)
    else:
      led.off()
    time.sleep(5)

if __name__ == '__main__':
  connect_internet()
  loop()