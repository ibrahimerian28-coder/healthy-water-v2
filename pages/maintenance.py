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

    customer_options = {}

    if "name" in df_c.columns:

        for _, row in df_c.iterrows():

            customer_name = str(
                row.get("name", "")
            ).strip()

            if customer_name:

                label = customer_name

                if row.get("phone"):
                    label += f" | {row.get('phone')}"

                customer_options[label] = {
                    "uuid": row.get("uuid", ""),
                    "name": customer_name,
                    "phone": row.get("phone", ""),
                    "area": row.get("area", ""),
                    "device_type": row.get(
                        "device_type",
                        ""
                    )
                }

    # =========================
    # ADD MAINTENANCE
    # =========================

    with st.expander("➕ Add Maintenance Visit"):

        with st.form("add_maintenance"):

            selected_customer = st.selectbox(
                "Customer",
                list(customer_options.keys())
            )

            customer_data = customer_options[
                selected_customer
            ]

            customer_uuid = customer_data["uuid"]

            customer_name = customer_data["name"]

            customer_phone = customer_data["phone"]

            customer_area = customer_data["area"]

            customer_device = customer_data[
                "device_type"
            ]

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

            # =========================
            # PARTS USED
            # =========================

            st.subheader("🧩 Parts Used")

            col1, col2, col3 = st.columns(3)

            with col1:
                p1 = st.checkbox("P1")
                p2 = st.checkbox("P2")
                p3 = st.checkbox("P3")

            with col2:
                membrane = st.checkbox("Membrane")
                post_carbon = st.checkbox("Post Carbon")
                calcite = st.checkbox("Calcite")

            with col3:
                infrared = st.checkbox("Infrared")

            # =========================
            # LOAD INVENTORY
            # =========================

            inventory_gid = st.session_state.SHEETS["Inventory"]

            df_inventory = load_sheet(inventory_gid)

            inventory_items = []

            if "name" in df_inventory.columns:

                inventory_items = (
                    df_inventory["name"]
                    .dropna()
                    .astype(str)
                    .tolist()
                )

            other = st.selectbox(
                "Other Part",
                [""] + inventory_items
            )

            # =========================
            # NOTES
            # =========================

            notes = st.text_area("Notes")

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

                customer_uuid,
                customer_name,
                customer_phone,
                customer_area,
                customer_device,

                str(visit_date),

                visit_type,

                issue,

                str(p1),
                str(p2),
                str(p3),
                str(membrane),
                str(post_carbon),
                str(calcite),
                str(infrared),
                other,

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
    status_filter = st.selectbox(
        "Filter by Status",
        ["All", "Pending", "Done", "Cancelled"]
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
    # STATUS FILTER
    if status_filter != "All":
        df_m = df_m[df_m["status"] == status_filter]

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
            st.write(f"👤 Customer: {row.get('customer_name')}")
            st.write(f"📞 Phone: {row.get('customer_phone')}")
            st.write(f"📍 Area: {row.get('customer_area')}")
            st.write(f"⚙️ Device: {row.get('customer_device_type')}")


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
            new_status = st.selectbox(
                "Status",
                ["Pending", "Done", "Cancelled"],
                index=["Pending", "Done", "Cancelled"].index(
                    row.get("status", "Pending")
                ),
                key=f"status_{visit_uuid}"
            )

            if new_status != row.get("status"):
    
                update_row(
                    "Maintenance",
                    visit_uuid,
                    {"status": new_status}
                )

                st.success("✅ Status Updated")
                st.rerun()

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

                    ok = delete_row_by_uuid(
                        "Maintenance",
                        visit_uuid
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
