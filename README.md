# ADSB-Spoofing


# ML-Based GNSS/ADS-B Spoofing Detection

**Prepared by:**

* Adam Bosredon
* Miguel Monereo de la Sota
* Maxime Batista

---

## 🎯 Goal

Feed **30 days of historical OpenSky aircraft data** into a system, train an ML model to learn *normal* flight behavior, then detect spoofed/fake flight traces by flagging anomalies and explaining why they’re suspicious.

---

## ⚙️ Backend

**Framework:** FastAPI

**Endpoints:**

* `/train` – train ML model on historical data
* `/predict` – detect anomalies for new flights
* `/flights` – query available flight traces

**ML Models (options):**

* Isolation Forest
* Autoencoder
* Other anomaly detection methods

**Response Example:**

```json
{
  "flight_id": "ICAO24_ABC123",
  "spoofed": true,
  "reasons": [
    "Teleportation: 120km in 5s",
    "Altitude mismatch: 800m vs expected 50m"
  ]
}
```

---

## 🖥️ Frontend GUI

**Frameworks:**

* React + Tailwind
* MapLibre (open-source map rendering)

### Views

#### 1. Map View

* Aircraft shown as **icons**
* Spoofed flights → **red planes**
* Normal flights → **green planes**
* Hover/Click → Show metadata

#### 2. Sidebar Panel

* Flight details: ICAO24, callsign, country, altitude, speed
* Spoofing status: **Normal / Spoofed**
* Reasons list (pulled from ML explanations)

#### 3. Control Panel

* Options for filtering, selecting ML model, toggling spoofed flights


