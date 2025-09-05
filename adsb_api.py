import requests
import time
import os
import json

# Base URL
BASE_URL = "https://api.adsb.lol"

# Toulouse coordinates
TOULOUSE_LAT = 43.6045
TOULOUSE_LON = 1.4442
RADIUS_NM = 250  # max radius allowed by API
REFRESH_INTERVAL = 2  # seconds

def get_aircraft_near_toulouse():
    """
    Fetch all aircraft near Toulouse using the /v2/point endpoint.
    Returns a list of dicts with callsign, type, reg, lat, lon.
    """
    aircraft_list = []
    url = f"{BASE_URL}/v2/point/{TOULOUSE_LAT}/{TOULOUSE_LON}/{RADIUS_NM}"
    
    print(f"\n--- Making request to: {url} ---")  # Log URL
    try:
        response = requests.get(url)
        print(f"HTTP status code: {response.status_code}")  # Log status

        try:
            data = response.json()
            # Pretty print first 500 chars of JSON for inspection
            print(f"Raw JSON (truncated to 500 chars):\n{json.dumps(data)[:500]}\n")
        except Exception as e:
            print(f"Failed to parse JSON: {e}")
            data = []

        if isinstance(data, list):
            for plane in data:
                if isinstance(plane, dict):
                    aircraft_list.append({
                        "callsign": plane.get("callsign", "N/A"),
                        "type": plane.get("type", "N/A"),
                        "reg": plane.get("reg", "N/A"),
                        "lat": plane.get("lat", 0),
                        "lon": plane.get("lon", 0)
                    })
            print(f"Parsed {len(aircraft_list)} aircraft from response.")
        else:
            print("Response is not a list. No aircraft parsed.")
    
    except Exception as e:
        print(f"Exception during request: {e}")

    return aircraft_list

def clear_terminal():
    """Clear the terminal screen for a clean live display."""
    os.system('cls' if os.name == 'nt' else 'clear')

def live_aircraft_tracking():
    """Continuously fetch all aircraft in Toulouse airspace and print every REFRESH_INTERVAL seconds."""
    while True:
        aircraft_toulouse = get_aircraft_near_toulouse()
        clear_terminal()
        print(f"Aircraft near Toulouse ({len(aircraft_toulouse)} planes):")
        for plane in aircraft_toulouse:
            print(f"{plane['callsign']} | {plane['type']} | {plane['reg']} | {plane['lat']}, {plane['lon']}")
        print(f"\nRefreshing in {REFRESH_INTERVAL} seconds...")
        time.sleep(REFRESH_INTERVAL)

if __name__ == "__main__":
    live_aircraft_tracking()
