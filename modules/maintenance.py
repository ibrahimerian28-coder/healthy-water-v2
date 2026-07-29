import streamlit as st
import pandas as pd
import uuid
from datetime import datetime
import json
from utils.data_service import (
    load_sheet,
    add_row,
    update_row,
    delete_row_by_uuid
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
    # =========================
    # SORT VISITS
    # =========================

    if "visit_date" in df_m.columns:

        df_m["visit_date"] = pd.to_datetime(
            df_m["visit_date"],
            errors="coerce"
        )

        df_m = df_m.sort_values(
            by="visit_date",
            ascending=False
        ).reset_index(drop=True)
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

    with st.form("add_maintenance"):

        selected_customer = st.selectbox(
            "Customer",
            list(customer_options.keys())
        )

        customer_data = customer_options[selected_customer]

        customer_uuid = customer_data["uuid"]
        customer_name = customer_data["name"]
        customer_phone = customer_data["phone"]
        customer_area = customer_data["area"]
        customer_device = customer_data["device_type"]
    
        visit_date = st.date_input("Visit Date")
    
        visit_type = st.selectbox(
            "Visit Type",
            ["Maintenance", "Installation", "Emergency", "Inspection"]
        )
    
        issue = st.text_area("Problem Description")
    
        st.subheader("🧩 Parts Used")

        col1, col2 = st.columns(2)

        with col1:

            p1 = st.checkbox("P1")
            st.write("P1 =", p1)

            if p1:
                p1_qty = st.number_input(
                    "P1 Qty",
                    min_value=1,
                    value=1,
                    step=1,
                    key="p1_qty"
                )
            else:
                p1_qty = 0

            p2 = st.checkbox("P2")

            if p2:
                p2_qty = st.number_input(
                    "P2 Qty",
                    min_value=1,
                    value=1,
                    step=1,
                    key="p2_qty"
                )
            else:
                p2_qty = 0

            p3 = st.checkbox("P3")

            if p3:
                p3_qty = st.number_input(
                    "P3 Qty",
                    min_value=1,
                    value=1,
                    step=1,
                    key="p3_qty"
                )
            else:
                p3_qty = 0


        with col2:

            membrane = st.checkbox("Membrane")

            if membrane:
                membrane_qty = st.number_input(
                    "Membrane Qty",
                    min_value=1,
                    value=1,
                    step=1,
                    key="membrane_qty"
                )
            else:
                membrane_qty = 0

            post_carbon = st.checkbox("Post Carbon")

            if post_carbon:
                post_carbon_qty = st.number_input(
                    "Post Carbon Qty",
                    min_value=1,
                    value=1,
                    step=1,
                    key="post_carbon_qty"
                )
            else:
                post_carbon_qty = 0

            calcite = st.checkbox("Calcite")

            if calcite:
                calcite_qty = st.number_input(
                    "Calcite Qty",
                    min_value=1,
                    value=1,
                    step=1,
                    key="calcite_qty"
                )
            else:
                calcite_qty = 0

            infrared = st.checkbox("Infrared")

            if infrared:
                infrared_qty = st.number_input(
                    "Infrared Qty",
                    min_value=1,
                    value=1,
                    step=1,
                    key="infrared_qty"
                )
            else:
                infrared_qty = 0
    
        # =========================
        # LOAD INVENTORY ITEMS
        # =========================

        inventory_gid = st.session_state.SHEETS["Inventory"]
        df_inventory = load_sheet(inventory_gid)

        excluded_items = [
            "P1",
            "P2",
            "P3",
            "Membrane",
            "Post Carbon",
            "Calcite",
            "Infrared"
        ]

        inventory_items = []

        if "item_name" in df_inventory.columns:

            inventory_items = (
                df_inventory["item_name"]
                .dropna()
                .astype(str)
                .str.strip()
                .tolist()
            )

            excluded_items = {
                "p1",
                "p2",
                "p3",
                "membrane",
                "post carbon",
                "calcite",
                "infrared"
            }

            inventory_items = [
                item
                for item in inventory_items
                if item.strip().lower() not in excluded_items
            ]
            
      

        other_parts = st.multiselect(
            "Other Parts",
            sorted(inventory_items)
        )
    
        cost = st.text_input("Cost")
        technician = st.text_input("Technician")
        notes = st.text_area("Notes")
    
        # 🔥 لازم يكون موجود داخل الفورم 100%
        save = st.form_submit_button("Save Visit")
    
        if save:
            visit_uuid = str(uuid.uuid4())
            # =========================
            # USED PARTS
            # =========================

            used_parts = []

            # Parts الأساسية
            if p1:
                used_parts.append({
                    "item": "P1",
                    "qty": 1
                })

            if p2:
                used_parts.append({
                    "item": "P2",
                    "qty": 1
                })

            if p3:
                used_parts.append({
                    "item": "P3",
                    "qty": 1
                })

            if membrane:
                used_parts.append({
                    "item": "Membrane",
                    "qty": 1
                })

            if post_carbon:
                used_parts.append({
                    "item": "Post Carbon",
                    "qty": 1
                })

            if calcite:
                used_parts.append({
                    "item": "Calcite",
                    "qty": 1
                })

            if infrared:
                used_parts.append({
                    "item": "Infrared",
                    "qty": 1
                })

            # Other Parts
            for part in other_parts:

                used_parts.append({
                    "item": part,
                    "qty": 1
                })

            st.write(used_parts)
            created_at = datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            )
    
            new_row = [
                visit_uuid,
                customer_uuid,
                customer_name,
                str(visit_date),
                "",
                "Pending",
                str(p1),
                str(p2),
                str(p3),
                str(membrane),
                str(post_carbon),
                str(calcite),
                str(infrared),
                ", ".join(other_parts),
                cost,
                notes,
                technician,
                created_at,
                created_at,
                ""
            ]
    
            ok = add_row("Maintenance", new_row)
    
            if ok:
                st.success("✅ Maintenance Visit Added")
                st.rerun()
            else:
                st.error("❌ Failed To Save")

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
            row.get("name")
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
            st.write(f"👤 Customer: {row.get('name')}")


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
            status_options = [
                "Pending",
                "Done",
                "Cancelled"
            ]

            current_status = str(
                row.get("status", "Pending")
            ).strip()

            if current_status not in status_options:
                current_status = "Pending"

            new_status = st.selectbox(
                "Status",
                status_options,
                index=status_options.index(current_status),
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
