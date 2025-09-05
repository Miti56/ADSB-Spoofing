from trino_client import conn
import pandas as pd

def fetch_aircraft_data(limit=1000):
    cur = conn.cursor()
    query = f"SELECT * FROM aircraft LIMIT {limit}"
    cur.execute(query)
    data = cur.fetchall()
    columns = [desc[0] for desc in cur.description]
    df = pd.DataFrame(data, columns=columns)
    return df

if __name__ == "__main__":
    df = fetch_aircraft_data()
    print(df.head())
