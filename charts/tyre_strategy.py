"""
charts/tyre_strategy.py
-----------------------
Chart 2: Tyre strategy for all drivers — horizontal bars showing
which compound each driver used and for how many laps.
Classic F1 strategy visualisation.
"""

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import pandas as pd


COMPOUND_COLORS = {
    'SOFT':   '#E8002D',
    'MEDIUM': '#FFF200',
    'HARD':   '#EBEBEB',
    'INTER':  '#39B54A',
    'WET':    '#0067FF',
    'UNKNOWN': '#888888',
}


def plot_tyre_strategy(session):
    """
    Horizontal bar chart of tyre strategy for all drivers.
    Each segment = one stint on a given compound.
    """
    laps = session.laps.copy()
    laps['Compound'] = laps['Compound'].fillna('UNKNOWN').str.upper()

    drivers = laps['Driver'].unique()

    fig, ax = plt.subplots(figsize=(13, max(5, len(drivers) * 0.55)))
    fig.patch.set_facecolor('#15151E')
    ax.set_facecolor('#15151E')

    for i, driver in enumerate(drivers):
        driver_laps = laps[laps['Driver'] == driver].sort_values('LapNumber')
        if driver_laps.empty:
            continue

        # Detect stints: consecutive laps on the same compound
        driver_laps = driver_laps.copy()
        driver_laps['StintChange'] = (driver_laps['Compound'] != driver_laps['Compound'].shift()).cumsum()

        for _, stint in driver_laps.groupby('StintChange'):
            start_lap = stint['LapNumber'].min()
            end_lap   = stint['LapNumber'].max()
            compound  = stint['Compound'].iloc[0]
            color     = COMPOUND_COLORS.get(compound, '#888888')
            ax.barh(
                i, end_lap - start_lap + 1,
                left=start_lap - 1,
                color=color,
                edgecolor='#15151E',
                linewidth=0.5,
                height=0.7
            )

    ax.set_yticks(range(len(drivers)))
    ax.set_yticklabels(drivers, color='white', fontsize=9)
    ax.set_xlabel("Lap", color='#AAAAAA', fontsize=11)
    ax.set_title(f"Tyre Strategy  |  {session.event['EventName']} {session.event.year} — {session.name}",
                 color='white', fontsize=14, pad=12)
    ax.tick_params(colors='#AAAAAA')
    for spine in ax.spines.values():
        spine.set_edgecolor('#333333')
    ax.grid(axis='x', color='#2A2A35', linewidth=0.5)
    ax.invert_yaxis()

    legend_patches = [
        mpatches.Patch(color=v, label=k.title())
        for k, v in COMPOUND_COLORS.items() if k != 'UNKNOWN'
    ]
    ax.legend(handles=legend_patches, facecolor='#1E1E2A', edgecolor='#333333',
              labelcolor='white', fontsize=9, loc='lower right')

    plt.tight_layout()
    plt.show()
