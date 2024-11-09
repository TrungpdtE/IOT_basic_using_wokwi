# ifttt.py
import urequests as requests
import ujson
import time

# IFTTT settings
api_key = 'cUpCulQEkIuHcxCT0i5pkV'  # Thay thế bằng API key của bạn
event = "entry_count"
m_url = f"https://maker.ifttt.com/trigger/{event}/with/key/{api_key}"

# Function to alert IFTTT
def alert_entry_count(count):
    post_data = ujson.dumps({
        "value1": "Entry detected",
        "value2": str(count),  # Ensure count is sent as string
        "value3": str(time.time())  # Ensure timestamp is sent as string
    })
    response = requests.post(m_url, headers={'Content-Type': 'application/json'}, data=post_data)
    print("IFTTT Response code:", response.status_code)  # Print the response code for debugging
    if response.status_code != 200:
        print("Failed to send data to IFTTT")
    else:
        print("Response content:", response.text)  # Print the response content for debugging
    response.close()
