from flask import Flask, jsonify, render_template
from opensky_api import get_aircraft_near_toulouse
import random

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/planes')
def planes():
    aircraft_list = get_aircraft_near_toulouse()

    # Demo: randomly mark ~25% of planes as spoofed
    for plane in aircraft_list:
        plane['spoofed'] = random.choice([False, False, False, True])
    return jsonify(aircraft_list)

if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Separate port from ADSB.lol app
