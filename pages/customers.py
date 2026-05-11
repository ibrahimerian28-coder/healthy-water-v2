import streamlit as st
import pandas as pd
import uuid

from utils.data_service import (
    load_sheet,
    add_row,
    update_row,
    delete_row
)

from utils.constants import (
    AREAS,
    CUSTOMER_STATUS,
    DEVICE_TYPES
)

# =========================
# HELPERS
# =========================

def clean_phone(p):

    if pd.isna(p):
        return ""

    p = str(p).strip()

    if p.lower() in ["nan", "none"]:
        return ""

    return p

def wa_link(phone):

    phone = clean_phone(phone)

    phone = phone.replace(" ", "")

    if phone.startswith("0"):
        phone = "2" + phone

    return f"https://wa.me/{phone}"

# =========================
# APP
# =========================

def app():

    st.title("👥 Customers")

    gid = st.session_state.SHEETS["Customers"]

    df = load_sheet(gid)

    # =========================
    # CLEAN DATA
    # =========================

    df.columns = df.columns.str.strip()

    if "name" in df.columns:
        df = df[df["name"].astype(str).str.strip() != ""]

    if "status" in df.columns:
        df = df[df["status"].astype(str).str.lower() != "deleted"]

    df = df.reset_index(drop=True)

    # =========================
    # ADD CUSTOMER
    # =========================

    with st.expander("➕ Add Customer"):

        with st.form("add_customer"):

            name = st.text_input("Name")

            phone = st.text_input("Phone")
            phone1 = st.text_input("Phone 1")
            phone2 = st.text_input("Phone 2")
            phone3 = st.text_input("Phone 3")
            phone4 = st.text_input("Phone 4")

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

                    phone,
                    phone1,
                    phone2,
                    phone3,
                    phone4,

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
    # SEARCH
    # =========================

    search = st.text_input("🔍 Search")

    if search:

        df = df[
            df.astype(str)
            .apply(lambda x: x.str.contains(search, case=False))
            .any(axis=1)
        ]

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

                    ok = delete_row(
                        "Customers",
                        real_row_index
                    )

                    if ok:

                        st.success("Deleted")

                        st.rerun()

                    else:

                        st.error("Delete Failed")

            # EDIT
            with col2:

                if st.button(
                    "✏️ Edit",
                    key=f"edit_{customer_uuid}"
                ):

                    st.session_state.edit_data = row.to_dict()
                    st.session_state.edit_index = real_row_index

                    st.rerun()

    # =========================
    # EDIT FORM
    # =========================

    if "edit_data" in st.session_state:

        st.divider()

        st.subheader("✏️ Edit Customer")

        er = st.session_state.edit_data

        rid = st.session_state.edit_index

        with st.form("edit_form"):

            name = st.text_input("Name", er.get("name", ""))

            phone = st.text_input("Phone", er.get("phone", ""))
            phone1 = st.text_input("Phone 1", er.get("phone_1", ""))
            phone2 = st.text_input("Phone 2", er.get("phone_2", ""))
            phone3 = st.text_input("Phone 3", er.get("phone_3", ""))
            phone4 = st.text_input("Phone 4", er.get("phone_4", ""))

            address = st.text_input("Address", er.get("address", ""))

            current_area = er.get("area", "")

            if current_area not in AREAS:
                current_area = "Other"

            selected_area = st.selectbox(
                "Area",
                AREAS,
                index=AREAS.index(current_area)
            )

            custom_area = ""

            if selected_area == "Other":

                custom_area = st.text_input(
                    "Enter New Area",
                    er.get("area", "")
                )

            area = custom_area if custom_area else selected_area

            location_url = st.text_input(
                "Location URL",
                er.get("location_url", "")
            )

            current_install_date = er.get("install_date", "")

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
                er.get("cycle", "")
            )
            current_device = er.get("device_type", "")

            if current_device not in DEVICE_TYPES:
                current_device = "Other"

            selected_device = st.selectbox(
                "Device Type",
                DEVICE_TYPES,
                index=DEVICE_TYPES.index(current_device)
            )

            custom_device = ""

            if selected_device == "Other":

                custom_device = st.text_input(
                    "Enter New Device Type",
                    er.get("device_type", "")
                )

            device_type = (
                custom_device
                if custom_device
                else selected_device
            )

            current_status = er.get("status", "Active")

            if current_status not in CUSTOMER_STATUS:
                current_status = "Active"

            status = st.selectbox(
                "Status",
                CUSTOMER_STATUS,
                index=CUSTOMER_STATUS.index(current_status)
            )

            save = st.form_submit_button("Save Changes")

            if save:

                updated = [

                    name,
                    er.get("customer_id", ""),
                    er.get("display_id", ""),
                    er.get("uuid", ""),

                    phone,
                    phone1,
                    phone2,
                    phone3,
                    phone4,

                    address,
                    area,
                    location_url,

                    install_date,
                    cycle,
                    device_type,
                    status
                ]

                ok = update_row(
                    "Customers",
                    rid,
                    updated
                )

                if ok:

                    st.success("✅ Updated")

                    del st.session_state.edit_data
                    del st.session_state.edit_index

                    st.rerun()

                else:

                    st.error("❌ Update Failed")
