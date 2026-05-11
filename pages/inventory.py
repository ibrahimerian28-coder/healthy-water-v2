import streamlit as st
import pandas as pd

def app():

    st.title("📦 Inventory")

    gid = st.session_state.SHEETS["Inventory"]
    url = f"https://docs.google.com/spreadsheets/d/1RGDGJaP_lo2Fp2beLqAQvLulqMk2WDJKqLv2g34-ycc/export?format=csv&gid={gid}"

    df = pd.read_csv(url).fillna("")

    st.dataframe(df)
