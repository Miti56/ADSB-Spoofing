import json
import gzip
import os
import glob
import pandas as pd

# Top-level folder containing all trace subfolders
top_folder = "/home/miti/Documents/Github/ADSB-Spoofing/traces"
output_file = "merged_adsb_dataFull.csv"

# Recursively collect all JSON files in all subfolders
files = glob.glob(os.path.join(top_folder, "**", "trace_full_*.json"), recursive=True)

all_data = []

for file_path in files:
    # Handle gzip-compressed files if needed
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
