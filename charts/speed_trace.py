"""
charts/speed_trace.py
---------------------
Chart 3: Speed trace across a lap — shows speed (km/h) at every
point on track, with throttle and brake overlaid.
The most detailed chart: uses telemetry data (sampled at ~240Hz).
"""

import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import pandas as pd


def plot_speed_trace(session, driver_code: str = "VER"):
    """
    Plot speed, throttle, and brake for the driver's fastest lap.
    """
    driver_code = driver_code.upper()
    laps = session.laps.pick_driver(driver_code)

    if laps.empty:
        print(f"  No laps found for {driver_code}, skipping speed trace.")
        return

    # Use the fastest lap
    fastest_lap = laps.pick_fastest()
    if fastest_lap is None or fastest_lap.empty:
        print(f"  No fastest lap data for {driver_code}.")
        return

    try:
        tel = fastest_lap.get_telemetry()
    except Exception as e:
        print(f"  Could not get telemetry: {e}")
        return

    if tel is None or tel.empty:
        print(f"  No telemetry data available.")
        return

    lap_time = fastest_lap['LapTime']
    lap_time_str = str(lap_time).split('days ')[-1] if lap_time is not None else "N/A"

    fig = plt.figure(figsize=(14, 7))
    fig.patch.set_facecolor('#15151E')

    gs = gridspec.GridSpec(3, 1, height_ratios=[3, 1, 1], hspace=0.05)

    ax1 = fig.add_subplot(gs[0])  # speed
    ax2 = fig.add_subplot(gs[1], sharex=ax1)  # throttle
    ax3 = fig.add_subplot(gs[2], sharex=ax1)  # brake

    for ax in [ax1, ax2, ax3]:
        ax.set_facecolor('#15151E')
        ax.tick_params(colors='#AAAAAA', labelsize=8)
        for spine in ax.spines.values():
            spine.set_edgecolor('#333333')
        ax.grid(color='#2A2A35', linewidth=0.5)

    dist = tel['Distance']

    # Speed
    ax1.plot(dist, tel['Speed'], color='#E8002D', linewidth=1.2)
    ax1.set_ylabel("Speed (km/h)", color='#AAAAAA', fontsize=10)
    ax1.set_title(
        f"{driver_code} — Fastest Lap Speed Trace  |  "
        f"{session.event['EventName']} {session.event.year}  |  Lap time: {lap_time_str}",
        color='white', fontsize=13, pad=10
    )
    ax1.tick_params(labelbottom=False)

    # Throttle
    if 'Throttle' in tel.columns:
        ax2.fill_between(dist, tel['Throttle'], color='#39B54A', alpha=0.7)
        ax2.set_ylabel("Throttle %", color='#AAAAAA', fontsize=9)
        ax2.set_ylim(0, 105)
    ax2.tick_params(labelbottom=False)

    # Brake
    if 'Brake' in tel.columns:
        brake = tel['Brake'].astype(float)
        ax3.fill_between(dist, brake * 100, color='#FF8000', alpha=0.7)
        ax3.set_ylabel("Brake", color='#AAAAAA', fontsize=9)

    ax3.set_xlabel("Distance (m)", color='#AAAAAA', fontsize=10)

    plt.show()
