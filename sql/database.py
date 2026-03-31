"""
sql/database.py
---------------
Handles all SQLite database operations.

Schema:
  sessions  — one row per session loaded
  laps      — one row per lap per driver

This shows SQL skills: CREATE TABLE, INSERT, SELECT, JOIN.
"""

import sqlite3
import os
import pandas as pd


DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'f1_telemetry.db')


def init_db() -> sqlite3.Connection:
    """Create the database and tables if they don't exist yet."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Sessions table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sessions (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            year         INTEGER NOT NULL,
            race         TEXT    NOT NULL,
            session_type TEXT    NOT NULL,
            loaded_at    TEXT    DEFAULT (datetime('now')),
            UNIQUE(year, race, session_type)
        )
    """)

    # Laps table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS laps (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id   INTEGER NOT NULL REFERENCES sessions(id),
            driver       TEXT    NOT NULL,
            lap_number   INTEGER NOT NULL,
            lap_time_s   REAL,
            compound     TEXT,
            tyre_life    INTEGER,
            is_personal_best INTEGER DEFAULT 0
        )
    """)

    conn.commit()
    print(f"  Database ready at: data/f1_telemetry.db")
    return conn


def save_session_to_db(conn: sqlite3.Connection, session, year: int, race: str, session_type: str):
    """Save session + lap data into SQLite."""
    cursor = conn.cursor()

    # Upsert session row
    cursor.execute("""
        INSERT OR IGNORE INTO sessions (year, race, session_type)
        VALUES (?, ?, ?)
    """, (year, race, session_type))
    conn.commit()

    cursor.execute("""
        SELECT id FROM sessions WHERE year=? AND race=? AND session_type=?
    """, (year, race, session_type))
    session_id = cursor.fetchone()[0]

    # Delete old lap rows for this session (clean re-import)
    cursor.execute("DELETE FROM laps WHERE session_id = ?", (session_id,))

    # Insert laps
    laps = session.laps[['Driver', 'LapNumber', 'LapTime', 'Compound', 'TyreLife', 'IsPersonalBest']].copy()
    laps['LapTime_s'] = laps['LapTime'].dt.total_seconds()
    laps['IsPersonalBest'] = laps['IsPersonalBest'].astype(int)

    rows = []
    for _, lap in laps.iterrows():
        rows.append((
            session_id,
            lap['Driver'],
            int(lap['LapNumber']),
            lap['LapTime_s'] if pd.notna(lap['LapTime_s']) else None,
            lap['Compound'] if pd.notna(lap['Compound']) else None,
            int(lap['TyreLife']) if pd.notna(lap['TyreLife']) else None,
            int(lap['IsPersonalBest'])
        ))

    cursor.executemany("""
        INSERT INTO laps (session_id, driver, lap_number, lap_time_s, compound, tyre_life, is_personal_best)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, rows)

    conn.commit()
    print(f"  Saved {len(rows)} laps to database (session_id={session_id})")


def query_fastest_laps(year: int, race: str, session_type: str):
    """
    Example query: return fastest lap per driver for a session.
    Run this separately to explore stored data.
    """
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query("""
        SELECT l.driver, MIN(l.lap_time_s) AS fastest_lap_s, l.compound
        FROM laps l
        JOIN sessions s ON l.session_id = s.id
        WHERE s.year = ? AND s.race = ? AND s.session_type = ?
          AND l.lap_time_s IS NOT NULL
        GROUP BY l.driver
        ORDER BY fastest_lap_s ASC
    """, conn, params=(year, race, session_type))
    conn.close()
    return df


if __name__ == "__main__":
    # Quick test: print fastest laps from stored data
    df = query_fastest_laps(2024, "Monaco", "Q")
    print("\nFastest laps stored in DB:")
    print(df.to_string(index=False))
