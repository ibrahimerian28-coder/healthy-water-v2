import streamlit as st
import pandas as pd

def app():

    st.title("🔧 Maintenance")

    gid = st.session_state.SHEETS["Maintenance"]
    url = f"https://docs.google.com/spreadsheets/d/1RGDGJaP_lo2Fp2beLqAQvLulqMk2WDJKqLv2g34-ycc/export?format=csv&gid={gid}"

    df = pd.read_csv(url).fillna("")

    st.dataframe(df)
