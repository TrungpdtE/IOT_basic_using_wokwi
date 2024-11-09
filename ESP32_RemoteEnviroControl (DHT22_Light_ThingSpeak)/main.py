from machine import Pin
import network
import time
import dht
import wifi
import thing_speak as tsp

#setup pin
led_pin = 14
led = Pin(led_pin, Pin.OUT)
light_sensor_pin = 12
light_sensor = Pin(light_sensor_pin, Pin.IN)
dht_pin = 27
dht_sensor = dht.DHT22(Pin(dht_pin))


def connect_internet():
  print("Connecting to WiFi", end="")
  sta_if = network.WLAN(network.STA_IF)
  sta_if.active(True)
  sta_if.connect(wifi.ssid, wifi.password)
  while not sta_if.isconnected():
    print(".", end="")
    time.sleep(0.1)
  print(" Connected!")

def thingspeak_display():
  previous_light_state = -1
  while True:
    dht_sensor.measure()
    #temperature
    t = dht_sensor.temperature()
    #humidity
    h = dht_sensor.humidity()
    print(t, h)
    print("Update to thingspeak....")
    
    #light states change when the led turn on/off
    current_light_state = light_sensor.value()
    if(previous_light_state != current_light_state):
      previous_light_state = current_light_state
      tsp.update_all(t, h, current_light_state)
    else:
      tsp.update_temp_and_hum(t, h)
    time.sleep(5)
    
    #test read api
    last_command = tsp.read_command()
    if last_command is not None:
        if last_command == "100":
            led.on()
        elif last_command == "0":
            led.off()
    else:
        print("Invalid command received.")

    time.sleep(5)

if __name__ == "__main__":
  #connect wifi
  connect_internet()
  thingspeak_display()