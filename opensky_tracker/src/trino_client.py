from dotenv import load_dotenv
import os
from trino.dbapi import connect

# Load environment variables from .env
load_dotenv()

TRINO_USER = os.getenv("TRINO_USER")
TRINO_PASSWORD = os.getenv("TRINO_PASSWORD")

# Connect to Trino
conn = connect(
    host='trino.opensky-network.org',
    port=443,
    user=TRINO_USER,
    catalog='opensky',
    schema='public',
    http_scheme='https',
    auth=(TRINO_USER, TRINO_PASSWORD)
)

print("Connected to Trino successfully!")
