# 🏎 F1 Telemetry Dashboard

A Python tool that pulls real Formula 1 race data via the **FastF1** API, stores it in a local **SQLite** database, and generates detailed telemetry charts — lap times, tyre strategies, and speed traces.

---

## Charts

| Chart | What it shows |
|---|---|
| Lap Times | Lap-by-lap pace for a driver, coloured by tyre compound |
| Tyre Strategy | All drivers' stint lengths on each compound |
| Speed Trace | Speed, throttle & brake through every metre of the fastest lap |

---

## Tech Stack

| Layer | Tool |
|---|---|
| Data source | [FastF1](https://docs.fastf1.dev/) (F1 telemetry API) |
| Data storage | SQLite via Python's `sqlite3` |
| Charts | Matplotlib |
| Data processing | Pandas |
| Language | Python 3.10+ |

---

## Setup

**1. Clone the repo**
```bash
git clone https://github.com/YOUR_USERNAME/f1-telemetry-dashboard.git
cd f1-telemetry-dashboard
```

**2. Create a virtual environment (recommended)**
```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# Mac / Linux:
source venv/bin/activate
```

**3. Install dependencies**
```bash
pip install -r requirements.txt
```

---

## Usage

**Basic run** (defaults to 2024 Monaco Qualifying, Verstappen):
```bash
python main.py
```

**Custom session:**
```bash
python main.py --year 2024 --race Monza --session R --driver HAM
```

**Arguments:**

| Argument | Default | Options |
|---|---|---|
| `--year` | 2024 | Any F1 season year |
| `--race` | Monaco | Race name (e.g. Silverstone, Spa, Monza) |
| `--session` | Q | `R` Race, `Q` Qualifying, `FP1`, `FP2`, `FP3` |
| `--driver` | VER | 3-letter driver code: `VER`, `HAM`, `LEC`, `NOR`... |

> **Note:** The first time you run a session, FastF1 downloads and caches the data. This can take 1–2 minutes. Subsequent runs for the same session are instant.

---

## Project Structure

```
f1-telemetry-dashboard/
│
├── main.py                  # Entry point — run this
│
├── utils/
│   └── fetcher.py           # FastF1 API calls
│
├── sql/
│   └── database.py          # SQLite setup, insert & query functions
│
├── charts/
│   ├── lap_times.py         # Lap time evolution chart
│   ├── tyre_strategy.py     # Strategy bar chart
│   └── speed_trace.py       # Telemetry speed/throttle/brake chart
│
├── data/
│   ├── cache/               # FastF1 data cache (git-ignored)
│   └── f1_telemetry.db      # SQLite database (git-ignored)
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Query the Database Directly

After running the dashboard once, you can query the stored data:

```bash
python sql/database.py
```

Or open `data/f1_telemetry.db` in [DB Browser for SQLite](https://sqlitebrowser.org/) to explore it visually.

Example SQL query:
```sql
SELECT driver, MIN(lap_time_s) AS fastest_lap_s, compound
FROM laps
JOIN sessions ON laps.session_id = sessions.id
WHERE sessions.year = 2024 AND sessions.race = 'Monaco'
GROUP BY driver
ORDER BY fastest_lap_s ASC;
```

---

## Ideas for Extension

- Add a **qualifying head-to-head** comparison between two drivers
- Build a **web dashboard** using Flask or Streamlit
- Add **weather data** overlay on lap time charts
- Track **tyre degradation** curves across stints
- Extend the database to compare across **multiple seasons**

---

## Author

**Sanjam Indermeet Bedi**  
Electronics and Computer Engineering — BITS Pilani, Dubai Campus  
[LinkedIn](https://linkedin.com/in/YOUR_PROFILE) · [GitHub](https://github.com/YOUR_USERNAME)

---

## License

MIT — free to use and modify.
