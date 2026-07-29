import streamlit as st
import pandas as pd
import uuid

from utils.data_service import (
    load_sheet,
    add_row,
    update_row,
    delete_row_by_uuid
)

from utils.constants import (
    AREAS,
    CUSTOMER_STATUS,
    DEVICE_TYPES
)

from modules.components.customer_helpers import (
    clean_phone,
    wa_link
)
from modules.components.customer_data import load_customers
# =========================
# APP
# =========================

def app():
    
    st.title("👥 Customers")
    df = load_customers()

    
    # =========================
    # ADD CUSTOMER
    # =========================

    with st.expander("➕ Add Customer"):

        with st.container():

            with st.form("add_customer"):
    
                name = st.text_input("Name")
    
                phone = st.text_input("Phone", value="", help="Keep leading zero")
                phone1 = st.text_input("Phone 1", value="", help="Keep leading zero")
                phone2 = st.text_input("Phone 2", value="", help="Keep leading zero")
                phone3 = st.text_input("Phone 3", value="", help="Keep leading zero")
                phone4 = st.text_input("Phone 4", value="", help="Keep leading zero")
    
                address = st.text_input("Address")
                selected_area = st.selectbox(
                    "Area",
                    AREAS
                )
    
                custom_area = ""
    
                if selected_area == "Other":
    
                    custom_area = st.text_input(
                    "Enter New Area"
                    )
    
                area = custom_area if custom_area else selected_area
    
                location_url = st.text_input("Google Maps URL")
    
                install_date = st.date_input(
                    "Install Date",
                    value=None
                )
    
                if install_date:
                    install_date = str(install_date)
                else:
                    install_date = ""
                cycle = st.text_input("Cycle")
                selected_device = st.selectbox(
                    "Device Type",
                    DEVICE_TYPES
                )
    
                custom_device = ""
    
                if selected_device == "Other":
    
                    custom_device = st.text_input(
                        "Enter New Device Type"
                    )
    
                device_type = (
                    custom_device
                    if custom_device
                    else selected_device
                )
    
                status = st.selectbox(
                    "Status",
                    CUSTOMER_STATUS,
                    index=0
                )
    
                submit = st.form_submit_button("Save")
    
                if submit:
    
                    customer_uuid = str(uuid.uuid4())
    
                    new_row = [
                        name,
                        "",
                        "",
                        customer_uuid,
    
                        str(phone),
                        str(phone1),
                        str(phone2),
                        str(phone3),
                        str(phone4),
    
                        address,
                        area,
                        location_url,
    
                        install_date,
                        cycle,
                        device_type,
                        status
                    ]
    
                    ok = add_row("Customers", new_row)
    
                    if ok:
    
                        st.success("✅ Customer Added")
    
                        st.rerun()
    
                    else:
    
                        st.error("❌ Failed")

    st.divider()
    # =========================
    # search
    # =========================

   search = st.text_input("🔍 Search")

   df = search_customers(df, search)

    # =========================
    # CUSTOMERS LIST
    # =========================

    st.write("عدد العملاء:", len(df))

    for i in range(len(df)):

        row = df.iloc[i]

        name = str(row.get("name", "")).strip()

        if not name:
            continue

        area = str(row.get("area", "")).strip()

        customer_uuid = str(row.get("uuid", "")).strip()

        if not customer_uuid:
            customer_uuid = f"temp_{i}"

        display_id = str(row.get("display_id", "")).strip()

        if not display_id:
            display_id = str(i + 1)

        real_row_index = i + 2

        with st.expander(f"👤 {name} | 📍 {area} | 🆔 {display_id}"):

            # =========================
            # PHONES
            # =========================

            phones = [
                row.get("phone"),
                row.get("phone_1"),
                row.get("phone_2"),
                row.get("phone_3"),
                row.get("phone_4"),
            ]

            st.write("📞 Phones")

            for ph in phones:

                ph = clean_phone(ph)

                if ph:

                    col1, col2 = st.columns([1, 3])

                    col1.write(ph)

                    col2.markdown(
                        f"[📞 Call](tel:{ph}) | [💬 WhatsApp]({wa_link(ph)})"
                    )
            # =========================
            # LOAD MAINTENANCE VISITS FOR THIS CUSTOMER
            # =========================

            maintenance_gid = st.session_state.SHEETS["Maintenance"]
            df_m = load_sheet(maintenance_gid)

            df_m.columns = df_m.columns.str.strip()

            customer_visits = df_m[
                df_m["customer_uuid"].astype(str).str.strip() ==
                str(customer_uuid).strip()
            ].copy()

            if not customer_visits.empty:

                customer_visits["visit_date"] = pd.to_datetime(
                    customer_visits["visit_date"],
                    errors="coerce"
                )

                customer_visits = customer_visits.sort_values(
                    by="visit_date",
                    ascending=False
                )
          
            st.subheader("🛠 سجل الصيانات")

            if customer_visits.empty:

                st.info("لا توجد زيارات صيانة")

            else:

                def mark(v):

                    if str(v).strip() in ["1", "TRUE", "True", "true", "✓"]:
                        return "✅"

                    return "❌"

                table = pd.DataFrame({

                    "📅 التاريخ":
                        customer_visits["visit_date"].dt.strftime("%Y-%m-%d"),

                    "P1":
                        customer_visits["P1"].apply(mark),

                    "P2":
                        customer_visits["P2"].apply(mark),

                    "P3":
                        customer_visits["P3"].apply(mark),

                    "Membrane":
                        customer_visits["membrane"].apply(mark),

                    "Post Carbon":
                        customer_visits["post_carbon"].apply(mark),

                    "Calcite":
                        customer_visits["calcite"].apply(mark),

                    "Infrared":
                        customer_visits["infrared"].apply(mark),

                    "👨‍🔧 الفني":
                        customer_visits["technician"],

                    "💰 التكلفة":
                        customer_visits["amount"]

                })

                st.dataframe(
                    table,
                    use_container_width=True,
                    hide_index=True
                )

            # =========================
            # DETAILS
            # =========================

            if row.get("address"):
                st.write(f"🏠 {row.get('address')}")

            if row.get("install_date"):
                st.write(f"📅 {row.get('install_date')}")

            if row.get("cycle"):
                st.write(f"🔁 Cycle: {row.get('cycle')}")

            if row.get("status"):
                st.write(f"📌 {row.get('status')}")

            # =========================
            # LOCATION
            # =========================

            loc = str(row.get("location_url", "")).strip()

            if loc and loc.lower() != "nan":

                st.markdown(
                    f"[📍 Open Location]({loc})"
                )

            st.divider()

            # =========================
            # ACTIONS
            # =========================

            col1, col2 = st.columns(2)

            # DELETE
            with col1:

                if st.button(
                    "🗑️ Delete",
                    key=f"del_{customer_uuid}"
                ):

                    st.session_state[
                        f"confirm_delete_{customer_uuid}"
                    ] = True

                if st.session_state.get(
                    f"confirm_delete_{customer_uuid}",
                    False
                ):

                    st.warning(
                        "⚠️ Are you sure you want to delete this customer?"
                    )

                    col_yes, col_no = st.columns(2)

                    with col_yes:

                        if st.button(
                            "✅ Yes Delete",
                            key=f"yes_{customer_uuid}"
                        ):

                            ok = delete_row_by_uuid(
                                "Customers",
                                customer_uuid
                            )

                            if ok:

                                st.success("Deleted")

                                del st.session_state[
                                    f"confirm_delete_{customer_uuid}"
                                ]

                                st.rerun()

                            else:

                                st.error("Delete Failed")

                    with col_no:

                        if st.button(
                            "❌ Cancel",
                            key=f"cancel_{customer_uuid}"
                        ):

                            del st.session_state[
                                f"confirm_delete_{customer_uuid}"
                            ]

                            st.rerun()

            # EDIT
            with col2:

                if st.button(
                    "✏️ Edit",
                    key=f"edit_{customer_uuid}"
                ):

                    st.session_state.edit_data = row.to_dict()
                    st.session_state.edit_uuid = row.get("uuid")

                    st.rerun()
            # =========================
            # INLINE EDIT FORM
            # =========================

            if (
                "edit_uuid" in st.session_state
                and st.session_state.edit_uuid == row.get("uuid")
            ):

                st.divider()

                st.subheader("✏️ Edit Customer")

                with st.form(f"edit_form_{customer_uuid}"):

                    name = st.text_input(
                        "Name",
                        row.get("name", "")
                    )

                    phone = st.text_input(
                        "Phone",
                        row.get("phone", "")
                    )

                    phone1 = st.text_input(
                        "Phone 1",
                        row.get("phone_1", "")
                    )

                    phone2 = st.text_input(
                        "Phone 2",
                        row.get("phone_2", "")
                    )

                    phone3 = st.text_input(
                        "Phone 3",
                        row.get("phone_3", "")
                    )

                    phone4 = st.text_input(
                        "Phone 4",
                        row.get("phone_4", "")
                    )

                    address = st.text_input(
                        "Address",
                        row.get("address", "")
                    )

                    # AREA

                    current_area = row.get("area", "")

                    if current_area not in AREAS:
                        current_area = "Other"

                    selected_area = st.selectbox(
                        "Area",
                        AREAS,
                        index=AREAS.index(current_area),
                        key=f"area_{customer_uuid}"
                    )

                    custom_area = ""

                    if selected_area == "Other":

                        custom_area = st.text_input(
                            "Enter New Area",
                            row.get("area", "")
                        )
    
                    area = (
                        custom_area
                        if custom_area
                        else selected_area
                    )

                    location_url = st.text_input(
                        "Location URL",
                        row.get("location_url", "")
                    )

                    # INSTALL DATE

                    current_install_date = row.get(
                        "install_date",
                        ""
                    )

                    if current_install_date:

                        try:
                            current_install_date = pd.to_datetime(
                                current_install_date
                            ).date()

                        except:
                            current_install_date = None

                    else:
                        current_install_date = None

                    install_date = st.date_input(
                        "Install Date",
                        value=current_install_date
                    )

                    if install_date:
                        install_date = str(install_date)
                    else:
                        install_date = ""

                    cycle = st.text_input(
                        "Cycle",
                        row.get("cycle", "")
                    )

                    # DEVICE TYPE

                    current_device = row.get(
                        "device_type",
                        ""
                    )

                    if current_device not in DEVICE_TYPES:
                        current_device = "Other"

                    selected_device = st.selectbox(
                        "Device Type",
                        DEVICE_TYPES,
                        index=DEVICE_TYPES.index(current_device),
                        key=f"device_{customer_uuid}"
                    )

                    custom_device = ""

                    if selected_device == "Other":

                        custom_device = st.text_input(
                            "Enter New Device Type",
                            row.get("device_type", "")
                        )

                    device_type = (
                        custom_device
                        if custom_device
                        else selected_device
                    )

                    # STATUS

                    current_status = row.get(
                        "status",
                        "Active"
                    )

                    if current_status not in CUSTOMER_STATUS:
                        current_status = "Active"

                    status = st.selectbox(
                        "Status",
                        CUSTOMER_STATUS,
                        index=CUSTOMER_STATUS.index(
                            current_status
                        ),    
                        key=f"status_{customer_uuid}"
                    )

                    save = st.form_submit_button(
                        "Save Changes"
                    )

                    if save:

                        updated = {

                            "name": name,

                            "phone": str(phone),
                            "phone_1": str(phone1),
                            "phone_2": str(phone2),
                            "phone_3": str(phone3),
                            "phone_4": str(phone4),

                            "address": address,
                            "area": area,
                            "location_url": location_url,

                            "install_date": install_date,

                            "cycle": cycle,

                            "device_type": device_type,

                            "status": status
                        }
                        st.write(customer_uuid)
                        st.write(updated)
                        ok = update_row(
                            "Customers",
                            customer_uuid,
                            updated
                        )

                        if ok:

                            st.success("✅ Updated")

                            del st.session_state.edit_uuid

                            st.rerun()

                        else:

                            st.error("❌ Update Failed")

   
    
