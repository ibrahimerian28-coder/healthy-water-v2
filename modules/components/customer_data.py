import streamlit as st
import pandas as pd
from utils.data_service import load_sheet


def load_customers():

    gid = "Customers"

    df = load_sheet(
        st.session_state.SHEETS[gid]
    )

    df.columns = df.columns.str.strip()

    if "name" in df.columns:
        df = df[df["name"].astype(str).str.strip() != ""]

    if "status" in df.columns:
        df = df[
            df["status"]
            .astype(str)
            .str.lower()
            != "deleted"
        ]

    df = df.reset_index(drop=True)

    if "area" in df.columns:
        df = df.sort_values("area")

    return df
