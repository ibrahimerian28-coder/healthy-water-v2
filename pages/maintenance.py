import streamlit as st
from utils.data_service import load_sheet

def app():

    st.title("🔧 Maintenance")

    gid = st.session_state.SHEETS["Maintenance"]
    df = load_sheet(gid)

    st.subheader("Maintenance Records")
    st.dataframe(df)

    st.write("عدد السجلات:", len(df))
