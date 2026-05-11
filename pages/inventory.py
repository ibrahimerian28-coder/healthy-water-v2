import streamlit as st
from utils.data_service import load_sheet

def app():

    st.title("📦 Inventory")

    gid = st.session_state.SHEETS["Inventory"]
    df = load_sheet(gid)

    st.dataframe(df)

    st.write("عدد الأصناف:", len(df))
