import trino
import os

# Toulouse bounding box
LAT_MIN = 43.4
LAT_MAX = 43.8
LON_MIN = 1.2
LON_MAX = 1.7

# Connect to OpenSky Trino
conn = trino.dbapi.connect(
    host='trino.opensky-network.org',
    port=443,
    user=os.environ.get("OPENSKY_USER"),
    catalog='minio',
    schema='osky',
    http_scheme='https',
    auth=trino.auth.BasicAuthentication(
        os.environ.get("OPENSKY_USER"),
        os.environ.get("OPENSKY_PASS")
    )
)

def get_aircraft_near_toulouse():
    """
    Query OpenSky historical database for Toulouse airspace.
    Returns a list of dicts with callsign, lat, lon, altitude, velocity, spoofed.
    """
    aircraft_list = []
    query = f"""
        SELECT icao24, callsign, lat, lon, geoaltitude, velocity, heading, alert
        FROM state_vectors_data4
        WHERE lat BETWEEN {LAT_MIN} AND {LAT_MAX}
        AND lon BETWEEN {LON_MIN} AND {LON_MAX}
        AND time > (EXTRACT(EPOCH FROM current_timestamp) - 300)
    """

    try:
        cur = conn.cursor()
        cur.execute(query)
        rows = cur.fetchall()
        for row in rows:
            aircraft_list.append({
                "icao24": row[0],
                "callsign": row[1] or "N/A",
                "lat": row[2],
                "lon": row[3],
                "geoaltitude": row[4],
                "velocity": row[5],
                "heading": row[6],
                "spoofed": False,  # placeholder for spoof detection
                "alert": row[7]
            })
    except Exception as e:
        print(f"Error fetching aircraft: {e}")

    return aircraft_list
