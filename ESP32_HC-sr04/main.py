import machine
import time
import random


TRIG_PIN = 23
ECHO_PIN = 22
BUZZER_PIN = 27  


trig = machine.Pin(TRIG_PIN, machine.Pin.OUT)
echo = machine.Pin(ECHO_PIN, machine.Pin.IN)
buzzer = machine.Pin(BUZZER_PIN, machine.Pin.OUT)

def get_distance():
    trig.value(1)
    time.sleep_us(10)
    trig.value(0)

    pulse_start = time.ticks_us()
    while echo.value() == 0:
        pulse_start = time.ticks_us()

    pulse_end = time.ticks_us()
    while echo.value() == 1:
        pulse_end = time.ticks_us()

    pulse_duration = pulse_end - pulse_start
    distance = (pulse_duration * 0.0343) / 2
    return distance

def simulate_distance():
    return random.uniform(0, 200)

def buzz(duration):
    buzzer.value(1)  
    time.sleep(duration)
    buzzer.value(0)  


DISTANCE_THRESHOLD = 50 

while True:
   
    
 
    distance = simulate_distance()

    print("Distance:", distance, "cm")

   
    if distance < DISTANCE_THRESHOLD:
        print("Buzzer ON!")
        buzz(0.5)  
    else:
        print("Buzzer OFF!")

    time.sleep(1)  
