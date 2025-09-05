import pandas as pd

# Define realistic limits
MAX_SPEED = 1200        # km/h
MAX_ALTITUDE = 60000    # feet

# Example flight bounding box (replace with real zones if needed)
MIN_LAT, MAX_LAT = -90, 90
MIN_LON, MAX_LON = -180, 180

def location_valid(lat, lon):
    return MIN_LAT <= lat <= MAX_LAT and MIN_LON <= lon <= MAX_LON

def detect_spoofing(df: pd.DataFrame) -> pd.DataFrame:
    reasons_list = []

    for _, row in df.iterrows():
        reasons = []
        # Location check
        if not location_valid(row['latitude'], row['longitude']):
            reasons.append("Location outside valid flight zones")

        # Speed check
        if row['velocity'] and row['velocity'] > MAX_SPEED:
            reasons.append("Speed exceeds known aircraft limits")

        # Altitude check
        if row['geo_altitude'] and row['geo_altitude'] > MAX_ALTITUDE:
            reasons.append("Altitude exceeds known aircraft limits")

        reasons_list.append(reasons)

    df['spoofed_reasons'] = reasons_list
    df['spoofed'] = df['spoofed_reasons'].map(lambda x: len(x) > 0)
    return df[df['spoofed']]

if __name__ == "__main__":
    from fetch_data import fetch_aircraft_data
    df = fetch_aircraft_data(limit=500)
    spoofed_df = detect_spoofing(df)
    print(spoofed_df[['icao24', 'spoofed', 'spoofed_reasons']])
