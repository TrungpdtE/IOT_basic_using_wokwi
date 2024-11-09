from machine import Pin
import time
import urequests as requests
import ujson
import network
import wifi

# Pin configuration
led_pin = 14
sensor_pin = 12
led = Pin(led_pin, Pin.OUT)
sensor = Pin(sensor_pin, Pin.IN)

# IFTTT settings
api_key = 'cUpCulQEkIuHcxCT0i5pkV'
event = "motion_detection"
m_url = f"https://maker.ifttt.com/trigger/{event}/json/with/key/{api_key}"

def connect_internet():
    print("Connecting to WiFi", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(wifi.ssid, wifi.password)
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.1)
    print(" Connected!")


def alert_motion(value):
    timestamp = time.time()
    post_data = ujson.dumps({
        "value1": "522H0148, Motion detected!",   
        "value2": value,               
        "value3": timestamp 
    })
    response = requests.post(m_url, headers={'content-type': 'application/json'}, data=post_data)
    response.close()


def loop():
    while True:
        value = sensor.value()
        print("Sensor value:", value)
        if value == 1:
            led.on()
            print("Motion detected! Sending alert email...")
            alert_motion(value)
        else:
            led.off()
        time.sleep(5)

if __name__ == '__main__':
    connect_internet()
    loop()
