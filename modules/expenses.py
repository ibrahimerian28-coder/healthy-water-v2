import streamlit as st
from utils.data_service import load_sheet

def app():

    st.title("💵 Expenses")

    gid = st.session_state.SHEETS["Expenses"]
    df = load_sheet(gid)

    st.subheader("Expenses Table")
    st.dataframe(df)

    total = len(df)
    st.write("عدد المصروفات:", total)
