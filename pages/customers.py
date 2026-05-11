import streamlit as st
import uuid

from utils.data_service import (
    load_sheet,
    add_row
)

def app():

    st.title("👥 Customers")

    gid = st.session_state.SHEETS["Customers"]

    df = load_sheet(gid)

    # =========================
    # CLEAN DATA
    # =========================

    if "name" in df.columns:
        df = df[df["name"].astype(str).str.strip() != ""]

    df = df.reset_index(drop=True)

    # =========================
    # ADD CUSTOMER
    # =========================

    with st.expander("➕ Add Customer"):

        with st.form("add_customer"):

            name = st.text_input("Name")
            phone = st.text_input("Phone")
            address = st.text_input("Address")
            area = st.text_input("Area")

            submit = st.form_submit_button("Save")

            if submit:

                customer_uuid = str(uuid.uuid4())

                new_row = [
                    name,
                    "",
                    "",
                    customer_uuid,
                    phone,
                    "",
                    "",
                    "",
                    "",
                    address,
                    area,
                    "",
                    "",
                    "",
                    "نشط"
                ]

                ok = add_row("Customers", new_row)

                if ok:
                    st.success("✅ Customer Added")
                    st.rerun()

                else:
                    st.error("❌ Failed")

    st.divider()

    # =========================
    # SHOW CUSTOMERS
    # =========================

    st.write("عدد العملاء:", len(df))

    st.dataframe(df)
