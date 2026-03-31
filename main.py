"""
F1 Telemetry Dashboard
======================
Main entry point. Run this to fetch F1 data, store it in SQLite,
and generate charts.

Usage:
    python main.py
    python main.py --year 2024 --race Monaco --session Q
    python main.py --year 2024 --race Monza --session R --driver VER
"""

import argparse
from ai_model import load_model, predict_lap_time
from utils.fetcher import fetch_session
from sql.database import init_db, save_session_to_db
from charts.lap_times import plot_lap_times
from charts.tyre_strategy import plot_tyre_strategy
from charts.speed_trace import plot_speed_trace


def main():
    parser = argparse.ArgumentParser(description="F1 Telemetry Dashboard")
    parser.add_argument("--year",    type=int,   default=2024,    help="Season year")
    parser.add_argument("--race",    type=str,   default="Monaco", help="Race name")
    parser.add_argument("--session", type=str,   default="Q",     help="Session type: R, Q, FP1, FP2, FP3")
    parser.add_argument("--driver",  type=str,   default="VER",   help="Driver 3-letter code e.g. VER, HAM, LEC")
    args = parser.parse_args()

    model = load_model()

    print(f"\n{'='*50}")
    print(f"  F1 Telemetry Dashboard")
    print(f"  {args.year} {args.race} — Session: {args.session}")
    print(f"{'='*50}\n")

    # 1. Initialise the database
    print("[1/4] Setting up database...")
    conn = init_db()

    # 2. Fetch data via FastF1
    print(f"[2/4] Fetching session data (this may take a moment first time)...")
    session = fetch_session(args.year, args.race, args.session)
    if session is None:
        print("  ERROR: Could not fetch session. Check race name/year and try again.")
        return

    # 3. Save to SQLite
    print("[3/4] Saving lap data to database...")
    save_session_to_db(conn, session, args.year, args.race, args.session)
    conn.close()

    # 4. Generate charts
    print("[4/4] Generating charts...\n")
    plot_lap_times(session, args.driver, model)
    plot_tyre_strategy(session)
    plot_speed_trace(session, args.driver)

    print("\nDone! Close chart windows to exit.")


if __name__ == "__main__":
    main()
