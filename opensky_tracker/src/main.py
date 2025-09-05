from fetch_data import fetch_aircraft_data
from detection import detect_spoofing

def main():
    df = fetch_aircraft_data(limit=500)
    spoofed_df = detect_spoofing(df)

    if spoofed_df.empty:
        print("No spoofed aircraft detected.")
    else:
        print("Detected spoofed aircraft:")
        for _, row in spoofed_df.iterrows():
            print(f"Aircraft {row['icao24']} flagged as spoofed:")
            for reason in row['spoofed_reasons']:
                print(f"- {reason}")

if __name__ == "__main__":
    main()
