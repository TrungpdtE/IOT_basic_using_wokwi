from machine import Pin, ADC, PWM,SoftI2C
import time
import dht
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
# Pin configuration
LDR_PIN = 34        # GPIO pin for LDR
LED_PIN = 23        # GPIO pin for LED
SERVO_PIN = 22      # GPIO pin for Servo

# Initialize pins
ldr = ADC(Pin(LDR_PIN))  # LDR pin
ldr.atten(ADC.ATTN_11DB)  # Configure for full scale voltage (0-3.6V)
led = Pin(LED_PIN, Pin.OUT)
servo = PWM(Pin(SERVO_PIN), freq=50)  # Servo PWM frequency

# Function to control servo
def move_servo(angle):
    duty = int((angle / 180) * 102 + 26)  # Convert angle to duty cycle
    servo.duty(duty)
    
led = Pin(5, Pin.OUT)
sensor = dht.DHT22(Pin(14))
i2c_addr = 0x27
totalRows = 2
totalColumns = 16
i2c = SoftI2C(scl = Pin(19), sda = Pin(21), freq = 10000)
lcd = I2cLcd(i2c, i2c_addr, totalRows, totalColumns)
lcd.putstr("Hello")
h = -1
while True:
    ldr_value = ldr.read()  # Read LDR value
    print("LDR Value:", ldr_value)

    # Update LCD display with LDR value
    lcd.clear()
    lcd.putstr(f"LDR: {ldr_value}")

    if ldr_value < 300:
        led.value(1)            # Turn on LED
        move_servo(90)          # Open door (90 degrees)
        time.sleep(2)           # Keep door open for 2 seconds
        move_servo(0)           # Close door (0 degrees)
        led.value(0)            # Turn off LED
        time.sleep(2)           # Wait before the next check
    else:
        led.value(0)            # Ensure LED is off when no access is detected

    time.sleep(0.1)            # Short delay before next reading

