import streamlit as st
from utils.data_service import load_sheet

def app():

    st.title("🛒 Store")

    gid = st.session_state.SHEETS["Store_Products"]
    df = load_sheet(gid)

    st.dataframe(df)

    st.write("عدد المنتجات:", len(df))
