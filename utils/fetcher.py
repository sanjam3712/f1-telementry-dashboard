"""
utils/fetcher.py
----------------
Handles fetching F1 session data using the FastF1 library.
FastF1 acts as our API wrapper — it contacts F1's data servers
and returns structured data (laps, telemetry, weather, etc.)
"""

import fastf1
import os


def fetch_session(year: int, race: str, session_type: str):
    """
    Fetch an F1 session using FastF1.

    Args:
        year         : Season year, e.g. 2024
        race         : Race name, e.g. 'Monaco', 'Monza', 'Silverstone'
        session_type : 'R' (Race), 'Q' (Qualifying), 'FP1', 'FP2', 'FP3'

    Returns:
        A loaded FastF1 Session object, or None on failure.
    """
    # Set up a local cache folder so we don't re-download data every run
    cache_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'cache')
    os.makedirs(cache_path, exist_ok=True)
    fastf1.Cache.enable_cache(cache_path)

    try:
        session = fastf1.get_session(year, race, session_type)
        # load() fetches: laps, telemetry, weather, tyre data
        session.load(telemetry=True, weather=True, laps=True, messages=False)
        print(f"  Loaded: {session.event['EventName']} {year} — {session.name}")
        print(f"  Drivers in session: {list(session.laps['Driver'].unique())}")
        return session
    except Exception as e:
        print(f"  FastF1 error: {e}")
        return None
