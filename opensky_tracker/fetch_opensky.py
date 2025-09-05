import trino

# Connect to OpenSky Trino using ExternalAuthentication (same as CLI)
try:
    conn = trino.dbapi.connect(
        host='trino.opensky-network.org',
        port=443,
        user='adambos2002',  # your username, lowercase
        catalog='minio',
        schema='osky',
        http_scheme='https',
        auth=trino.auth.ExternalAuthentication()  # uses CLI/session credentials
    )
    cur = conn.cursor()
    print("✅ Connected to Trino successfully!")

    # Example query: get latest 5 state vectors
    query = """
    SELECT icao24, callsign, lat, lon, velocity, geoaltitude, baroaltitude, time
    FROM state_vectors_data4
    ORDER BY time DESC
    LIMIT 5
    """
    cur.execute(query)
    rows = cur.fetchall()
    
    print("Latest 5 state vectors:")
    for row in rows:
        print(row)

except trino.exceptions.HttpError as e:
    print(f"HTTP Error: {e}")

except Exception as e:
    print(f"Unexpected error: {e}")
