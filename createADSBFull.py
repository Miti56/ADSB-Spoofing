import gzip
import os
import glob
import pandas as pd
import ijson  # streaming JSON parser

top_folder = "/home/miti/Documents/Github/ADSB-Spoofing/traces"
output_file = "merged_adsb_data.csv"
batch_size = 100000  # adjust depending on RAM
files = glob.glob(os.path.join(top_folder, "**", "trace_full_*.json"), recursive=True)

# Initialize output CSV with header once
header_written = False
batch = []

def save_batch(batch, mode="a"):
    global header_written
    df = pd.DataFrame(batch)
    df.to_csv(output_file, mode=mode, index=False, header=not header_written)
    header_written = True

for file_path in files:
    try:
        with gzip.open(file_path, "rt") as f:
            parser = ijson.items(f, "")
            data = next(parser)
    except OSError:
        with open(file_path, "r") as f:
            parser = ijson.items(f, "")
            data = next(parser)

    icao = data.get("icao")
    flight = data.get("r")
    aircraft_type = data.get("t")
    desc = data.get("desc")

    # Stream through "trace" array
    for point in data["trace"]:
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
            batch.append(record)

        # Write batch to disk periodically
        if len(batch) >= batch_size:
            save_batch(batch)
            batch = []

# Save remaining
if batch:
    save_batch(batch)

print(f"Finished extracting ADS-B traces into {output_file}")
