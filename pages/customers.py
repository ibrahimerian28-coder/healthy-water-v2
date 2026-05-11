import streamlit as st
import pandas as pd
import uuid

def app():

    st.title("👥 Customers Management")

    # =========================
    # LOAD DATA FROM SESSION
    # =========================
    gid = st.session_state.SHEETS["Customers"]
    url = f"https://docs.google.com/spreadsheets/d/1RGDGJaP_lo2Fp2beLqAQvLulqMk2WDJKqLv2g34-ycc/export?format=csv&gid={gid}"

    df = pd.read_csv(url).fillna("")
    df.columns = df.columns.str.strip()

    st.write("عدد العملاء:", len(df))

    # =========================
    # DISPLAY ONLY (مرحلة 1)
    # =========================
    for i, row in df.iterrows():

        st.write(f"👤 {row.get('name')} | 📍 {row.get('area')}")
