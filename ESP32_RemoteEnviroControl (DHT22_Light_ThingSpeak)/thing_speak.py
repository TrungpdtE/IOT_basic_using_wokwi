import urequests as requests

api_key = "0IZMLPWM09KAM273"

def update_temp_and_hum(new_temp, new_hum):
    res = requests.get(f'https://api.thingspeak.com/update?api_key={api_key}&field1={new_temp}&field2={new_hum}')
    data = res.text
    if(data == '0'):
        print("Update failed!")
    else:
        print("Update successful!")

def update_all(new_temp, new_hum, new_light):
    res = requests.get(f'https://api.thingspeak.com/update?api_key={api_key}&field1={new_temp}&field2={new_hum}&field3={new_light}')
    data = res.text
    if(data == '0'):
        print("Update failed!")
    else:
        print("Update successful!")

def update_light_state(state):
    res = requests.get(f'https://api.thingspeak.com/update?api_key={api_key}&field3={state}')
    data = res.text
    if(data == '0'):
        print("Update failed!")
    else:
        print("Update successful!")

def read_command():
    res = requests.get(f"https://api.thingspeak.com/channels/2710994/fields/4/last.json?api_key={api_key}").json()
    print("API Response:", res)  # Debugging line
    if isinstance(res, dict) and 'field4' in res:
        return res['field4']
    else:
        print("Unexpected API response:", res)
        return None  # Hoặc giá trị mặc định khác
