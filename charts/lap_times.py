"""
charts/lap_times.py
-------------------
Chart 1: Lap time evolution for a given driver across a session.
Shows how tyre degradation and strategy affect pace.
"""

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import pandas as pd


# Official F1 team colours (used for driver lines)
DRIVER_COLORS = {
    "VER": "#3671C6", "PER": "#3671C6",   # Red Bull
    "HAM": "#27F4D2", "RUS": "#27F4D2",   # Mercedes
    "LEC": "#E8002D", "SAI": "#E8002D",   # Ferrari
    "NOR": "#FF8000", "PIA": "#FF8000",   # McLaren
    "ALO": "#358C75", "STR": "#358C75",   # Aston Martin
    "GAS": "#0093CC", "OCO": "#0093CC",   # Alpine
    "ALB": "#64C4FF", "SAR": "#64C4FF",   # Williams
    "TSU": "#356FAD", "RIC": "#356FAD",   # RB
    "HUL": "#B6BABD", "MAG": "#B6BABD",  # Haas
    "BOT": "#52E252", "ZHO": "#52E252",   # Kick Sauber
}
DEFAULT_COLOR = "#AAAAAA"


def plot_lap_times(session, driver_code: str = "VER"):
    """
    Plot lap time evolution for one driver, coloured by tyre compound.
    """
    driver_code = driver_code.upper()
    laps = session.laps.pick_driver(driver_code)

    if laps.empty:
        print(f"  No lap data found for driver: {driver_code}")
        print(f"  Available drivers: {list(session.laps['Driver'].unique())}")
        return

    laps = laps.copy()
    laps['LapTime_s'] = laps['LapTime'].dt.total_seconds()
    laps = laps.dropna(subset=['LapTime_s'])

    compound_colors = {
        'SOFT':  '#E8002D',
        'MEDIUM': '#FFF200',
        'HARD':  '#FFFFFF',
        'INTER': '#39B54A',
        'WET':   '#0067FF',
    }

    fig, ax = plt.subplots(figsize=(12, 5))
    fig.patch.set_facecolor('#15151E')
    ax.set_facecolor('#15151E')

    compounds = laps['Compound'].unique()
    for compound in compounds:
        subset = laps[laps['Compound'] == compound]
        color = compound_colors.get(str(compound).upper(), DEFAULT_COLOR)
        ax.scatter(
            subset['LapNumber'], subset['LapTime_s'],
            color=color, label=str(compound).title(),
            s=40, zorder=3, edgecolors='none'
        )
        ax.plot(
            subset['LapNumber'], subset['LapTime_s'],
            color=color, alpha=0.4, linewidth=1
        )

    # Fastest lap marker
    fastest_idx = laps['LapTime_s'].idxmin()
    fastest = laps.loc[fastest_idx]
    ax.scatter(fastest['LapNumber'], fastest['LapTime_s'],
               color='#FFFFFF', s=120, zorder=5, marker='*',
               label=f"Fastest: {fastest['LapTime_s']:.3f}s")

    driver_color = DRIVER_COLORS.get(driver_code, DEFAULT_COLOR)
    ax.set_title(f"{driver_code} — Lap Times  |  {session.event['EventName']} {session.event.year}",
                 color='white', fontsize=14, pad=12)
    ax.set_xlabel("Lap Number", color='#AAAAAA', fontsize=11)
    ax.set_ylabel("Lap Time (s)", color='#AAAAAA', fontsize=11)
    ax.tick_params(colors='#AAAAAA')
    for spine in ax.spines.values():
        spine.set_edgecolor('#333333')
    ax.grid(color='#2A2A35', linewidth=0.5)
    ax.legend(facecolor='#1E1E2A', edgecolor='#333333', labelcolor='white', fontsize=9)

    plt.tight_layout()
    plt.show()
