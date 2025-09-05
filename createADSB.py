import json
import gzip
import os
import glob
import pandas as pd

# Folder containing all your trace JSON files
folder_path = "/home/miti/Documents/Github/ADSB-Spoofing/traces1folder/f1"
output_file = "merged_adsb_dataSMALL.csv"

# Collect all JSON files
files = glob.glob(os.path.join(folder_path, "trace_full_*.json"))

all_data = []

for file_path in files:
    # If the files are gzip compressed, use gzip.open; otherwise, use open
    try:
        with gzip.open(file_path, "rt") as f:
            data = json.load(f)
    except OSError:
        with open(file_path, "r") as f:
            data = json.load(f)

    icao = data.get("icao")
    flight = data.get("r")
    aircraft_type = data.get("t")
    desc = data.get("desc")

    trace = data.get("trace", [])
    
    for point in trace:
        # ADS-B info is usually in the 9th element (index 8) of the point
        adsb = point[8]
        if adsb:
            record = {
                "icao": icao,
                "flight": flight,
                "aircraft_type": aircraft_type,
                "desc": desc,
                "timestamp_offset": point[0],
                "lat": point[1],
                "lon": point[2],
                "alt": point[3],
                "ground_speed": point[4],
                "track": point[5],
                "geom_rate": point[7],
                "adsb_type": adsb.get("type"),
                "true_heading": adsb.get("true_heading"),
                "mag_heading": adsb.get("mag_heading"),
                "squawk": adsb.get("squawk"),
                "emergency": adsb.get("emergency"),
                "category": adsb.get("category"),
                "nav_qnh": adsb.get("nav_qnh"),
                "alert": adsb.get("alert"),
                "spi": adsb.get("spi"),
                "nic": adsb.get("nic"),
                "rc": adsb.get("rc"),
                "nac_p": adsb.get("nac_p"),
                "nac_v": adsb.get("nac_v"),
                "sil": adsb.get("sil"),
                "sil_type": adsb.get("sil_type"),
                "gva": adsb.get("gva"),
                "sda": adsb.get("sda")
            }
            all_data.append(record)

# Convert to DataFrame and save as CSV
df = pd.DataFrame(all_data)
df.to_csv(output_file, index=False)
print(f"Merged dataset saved to {output_file}, total records: {len(df)}")
