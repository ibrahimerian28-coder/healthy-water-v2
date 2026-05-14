import streamlit as st
import pandas as pd
import uuid
from datetime import datetime

from utils.data_service import (
    load_sheet,
    add_row,
    update_row,
    delete_row
)

# =========================
# APP
# =========================

def app():

    st.title("🔧 Maintenance")

    # =========================
    # LOAD DATA
    # =========================

    maintenance_gid = st.session_state.SHEETS["Maintenance"]
    customers_gid = st.session_state.SHEETS["Customers"]

    df_m = load_sheet(maintenance_gid)
    df_c = load_sheet(customers_gid)

    # =========================
    # CLEAN DATA
    # =========================

    df_m.columns = df_m.columns.str.strip()
    df_c.columns = df_c.columns.str.strip()

    # =========================
    # CUSTOMERS LIST
    # =========================

    customer_names = []

    if "name" in df_c.columns:

        customer_names = (
            df_c["name"]
            .dropna()
            .astype(str)
            .tolist()
        )

    # =========================
    # ADD MAINTENANCE
    # =========================

    with st.expander("➕ Add Maintenance Visit"):

        with st.form("add_maintenance"):

            customer_name = st.selectbox(
                "Customer",
                customer_names
            )

            visit_date = st.date_input(
                "Visit Date"
            )

            visit_type = st.selectbox(
                "Visit Type",
                [
                    "Maintenance",
                    "Installation",
                    "Emergency",
                    "Inspection"
                ]
            )

            issue = st.text_area(
                "Problem Description"
            )

            replaced_parts = st.text_area(
                "Replaced Parts"
            )

            cost = st.text_input(
                "Cost"
            )

            technician = st.text_input(
                "Technician"
            )

            notes = st.text_area(
                "Notes"
            )

            save = st.form_submit_button(
                "Save Visit"
            )

            if save:

                visit_uuid = str(uuid.uuid4())

                new_row = [

                    visit_uuid,
                    customer_name,
                    str(visit_date),
                    visit_type,
                    issue,
                    replaced_parts,
                    cost,
                    technician,
                    notes
                ]

                ok = add_row(
                    "Maintenance",
                    new_row
                )

                if ok:

                    st.success(
                        "✅ Maintenance Visit Added"
                    )

                    st.rerun()

                else:

                    st.error(
                        "❌ Failed To Save"
                    )

    st.divider()

    # =========================
    # SEARCH
    # =========================

    search = st.text_input(
        "🔍 Search Maintenance"
    )

    if search:

        df_m = df_m[
            df_m.astype(str)
            .apply(
                lambda x: x.str.contains(
                    search,
                    case=False
                )
            )
            .any(axis=1)
        ]

    # =========================
    # VISITS LIST
    # =========================

    st.write(
        "عدد الزيارات:",
        len(df_m)
    )

    for i in range(len(df_m)):

        row = df_m.iloc[i]

        customer_name = str(
            row.get("customer_name", "")
        )

        visit_date = str(
            row.get("visit_date", "")
        )

        visit_type = str(
            row.get("visit_type", "")
        )

        visit_uuid = str(
            row.get("uuid", "")
        )

        if not visit_uuid:
            visit_uuid = f"visit_{i}"

        real_row_index = i + 2

        with st.expander(
            f"🔧 {customer_name} | 📅 {visit_date} | {visit_type}"
        ):

            if row.get("issue"):
                st.write(
                    f"⚠️ Problem: {row.get('issue')}"
                )

            if row.get("replaced_parts"):
                st.write(
                    f"🧩 Parts: {row.get('replaced_parts')}"
                )

            if row.get("cost"):
                st.write(
                    f"💰 Cost: {row.get('cost')}"
                )

            if row.get("technician"):
                st.write(
                    f"👨‍🔧 Technician: {row.get('technician')}"
                )

            if row.get("notes"):
                st.write(
                    f"📝 Notes: {row.get('notes')}"
                )

            st.divider()

            col1, col2 = st.columns(2)

            # DELETE
            with col1:

                if st.button(
                    "🗑️ Delete",
                    key=f"del_{visit_uuid}"
                ):

                    ok = delete_row(
                        "Maintenance",
                        real_row_index
                    )

                    if ok:

                        st.success("Deleted")

                        st.rerun()

                    else:

                        st.error("Delete Failed")

            # EDIT
            with col2:

                st.info(
                    "Edit Coming Soon"
                )
