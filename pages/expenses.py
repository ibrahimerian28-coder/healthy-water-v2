import streamlit as st
import pandas as pd

def app():

    st.title("💵 Expenses")

    try:
        gid = st.session_state.SHEETS["Expenses"]

        url = f"https://docs.google.com/spreadsheets/d/1RGDGJaP_lo2Fp2beLqAQvLulqMk2WDJKqLv2g34-ycc/export?format=csv&gid={gid}"

        df = pd.read_csv(url).fillna("")
        df.columns = df.columns.str.strip()

        st.subheader("📊 Expenses Data")
        st.dataframe(df)

        st.write("عدد السجلات:", len(df))

    except Exception as e:
        st.error(f"Error loading expenses: {e}")
