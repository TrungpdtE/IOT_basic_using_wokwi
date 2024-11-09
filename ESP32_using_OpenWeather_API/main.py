import time
import network
import urequests as requests
from machine import Pin, SoftI2C
from lcd_api import LcdApi
from i2c_lcd import I2cLcd  # Đảm bảo tên thư viện là chính xác

# Kết nối WiFi
ssid = 'Wokwi-GUEST'
password = ''

print("Connecting to WiFi", end="")
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(ssid, password)

while not sta_if.isconnected():
    print(".", end="")
    time.sleep(0.1)

print(" Connected!")

# Cấu hình API
my_id = "fea7b349dc6d52fee018704f8f5ffd40"
my_url = f"https://api.openweathermap.org/data/2.5/weather?id=1566083&appid={my_id}&lang=vi&units=metric"
my_city = "HaNoi"
api_url = "https://timeapi.io/api/Time/current/zone?timeZone=Asia/Bangkok"

# Khởi tạo LCD
i2c = SoftI2C(scl=Pin(23), sda=Pin(21))  # Gán chân SCL là 23 và SDA là 21
lcd = I2cLcd(i2c, 0x27, 2, 16)  # Địa chỉ I2C và kích thước LCD

while True:
    # Lấy thời gian hiện tại
    response = requests.get(api_url).json()
    hour = response['hour']
    minute = response['minute']

    lcd.move_to(0, 0)
    lcd.putstr(f"{my_city}, {hour}:{minute}")

    # Cập nhật thời tiết mỗi 5 giây
    res = requests.get(my_url).json()
    print("Current weather:", res['weather'][0]["description"])

    # Nhiệt độ
    temperature = res['main']['temp']
    print("Temperature:", temperature)

    # Độ ẩm
    humidity = res['main']['humidity']
    print("Humidity:", humidity)

    lcd.move_to(0, 1)
    lcd.putstr(f"T: {temperature}, H: {humidity}")

    time.sleep(5)  # Thời gian chờ trước khi lặp lại
