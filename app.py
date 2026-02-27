"""
Urban Longevity - Streamlit Dashboard
Solving the Green Paradox: optimize tree planting to reduce PM2.5 without triggering pollen-induced asthma.
"""

import streamlit as st
import plotly.express as px
import pandas as pd
from pathlib import Path

# --- Page config ---
st.set_page_config(page_title="Urban Longevity", layout="wide")

# --- Paths ---
DATA_DIR = Path(__file__).resolve().parent
MASTER_CSV = DATA_DIR / "manhattan_master.csv"

# --- Mock recommendation logic (no live pollen DB) ---
def recommended_action(asthma_rate: float, median_asthma: float) -> str:
    if asthma_rate > median_asthma:
        return "High Risk: Plant strictly Low-Pollen female trees (e.g., Female Ginkgo or Red Maple)."
    return "Monitor: Safe for standard green infrastructure."


def main():
    st.title("Urban Longevity: Solving the Green Paradox")
    st.subheader(
        "Optimizing tree planting to reduce PM2.5 without triggering pollen-induced asthma. "
        "Use the map to identify high-risk zip codes and recommended actions."
    )

    # Load data
    if not MASTER_CSV.exists():
        st.error(f"Master dataset not found: {MASTER_CSV}. Run `python data_prep.py` first.")
        return

    df = pd.read_csv(MASTER_CSV)
    df["zip"] = df["zip"].astype(int)
    median_asthma = df["asthma_rate_per_10k"].median()
    df["Recommended_Action"] = df["asthma_rate_per_10k"].apply(
        lambda r: recommended_action(r, median_asthma)
    )

    # Scatter map: lat/lon, color=pm25 (red/dark for high), size=tree_count
    fig = px.scatter_mapbox(
        df,
        lat="latitude",
        lon="longitude",
        color="pm25",
        size="tree_count",
        color_continuous_scale="RdYlGn_r",  # red = high, green = low
        size_max=30,
        mapbox_style="open-street-map",
        hover_data={
            "zip": True,
            "pm25": ":.2f",
            "asthma_rate_per_10k": ":.2f",
            "tree_count": True,
            "Recommended_Action": True,
            "latitude": False,
            "longitude": False,
        },
        labels={
            "pm25": "PM2.5 (mcg/m³)",
            "asthma_rate_per_10k": "Asthma rate (per 10k)",
            "tree_count": "Tree count",
            "zip": "Zip Code",
        },
    )
    fig.update_layout(
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
        coloraxis_colorbar_title="PM2.5",
    )

    st.plotly_chart(fig, use_container_width=True)


if __name__ == "__main__":
    main()
