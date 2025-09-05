import requests

# Example ICAO hex code
icao_hex = "4CA87C"

# API endpoint
url = f"https://api.adsb.lol/v2/icao/{icao_hex}"

# Send GET request
response = requests.get(url)

# Check if request was successful
if response.status_code == 200:
    data = response.json()
    print("Aircraft Data:", data)
else:
    print("Error:", response.status_code, response.text)
