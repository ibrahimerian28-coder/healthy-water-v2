import streamlit as st
from utils.data_service import load_sheet

def app():

    st.title("👥 Customers")

    gid = st.session_state.SHEETS["Customers"]
    df = load_sheet(gid)

    df = df[df["name"].astype(str).str.strip() != ""]
    df = df.reset_index(drop=True)

    st.subheader("📋 Customers List")
    st.dataframe(df)

    st.write("عدد العملاء:", len(df))
