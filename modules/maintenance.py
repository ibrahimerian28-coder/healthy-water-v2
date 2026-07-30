import streamlit as st
import pandas as pd
import uuid
from datetime import datetime
import json
from components.parts_manager import render_parts_manager
from utils.data_service import (
    load_sheet,
    add_row,
    update_row,
    delete_row_by_uuid
)
from utils.inventory_service import (
    check_inventory,
    deduct_inventory
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

    
    # =========================
    # LOAD INVENTORY
    # =========================

    inventory_gid = st.session_state.SHEETS["Inventory"]
    df_inventory = load_sheet(inventory_gid)
    
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
    used_parts = render_parts_manager(df_inventory)
    

    cost = st.text_input("Cost")
    technician = st.text_input("Technician")
    notes = st.text_area("Notes")

    # 🔥 لازم يكون موجود داخل الفورم 100%
    save = st.button(
        "💾 Save Visit",
        type="primary",
        use_container_width=True
    )
    
    if save:

        visit_uuid = str(uuid.uuid4())
    
        created_at = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )
    
        # القيم الافتراضية
        new_p1 = ""
        new_p2 = ""
        new_p3 = ""
        new_membrane = ""
        new_post_carbon = ""
        new_calcite = ""
        new_infrared = ""
    
        other_parts = []
    
        # استخراج البيانات من used_parts
        for part in used_parts:
    
            name = part["item"].strip().lower()
    
            if name == "p1":
                new_p1 = "TRUE"
    
            elif name == "p2":
                new_p2 = "TRUE"
    
            elif name == "p3":
                new_p3 = "TRUE"
    
            elif name == "membrane":
                new_membrane = "TRUE"
    
            elif name == "post carbon":
                new_post_carbon = "TRUE"
    
            elif name == "calcite":
                new_calcite = "TRUE"
    
            elif name == "infrared":
                new_infrared = "TRUE"
    
            else:
                other_parts.append(part["item"])
        errors = check_inventory(
            used_parts,
            inventory_gid
        )
        
        if errors:
        
            st.error("❌ لا يمكن حفظ الزيارة")
        
            for err in errors:
                st.warning(err)
        
            st.stop()
        st.write("RETURN USED PARTS")
        st.json(used_parts)
    
        new_row = [
    
            visit_uuid,
            customer_uuid,
            customer_name,
            str(visit_date),
            "",
            "Pending",
    
            new_p1,
            new_p2,
            new_p3,
            new_membrane,
            new_post_carbon,
            new_calcite,
            new_infrared,
    
            ", ".join(other_parts),
    
            cost,
            notes,
            technician,
            created_at,
            created_at,
    
            json.dumps(
                used_parts,
                ensure_ascii=False
            )
        ]
    
        ok = add_row(
            "Maintenance",
            new_row
        )
    
        if ok:

            deduct_inventory(
                used_parts,
                inventory_gid
            )
        
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
