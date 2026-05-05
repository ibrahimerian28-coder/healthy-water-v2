import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta

# =========================
# CONFIG
# =========================

st.set_page_config(page_title="Healthy Water Pro", layout="wide")

WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwPIG6-S1aOxIL5KvN-XF_zwW0Xu6U9ARLau_R21s_Z9MJafWuPZW8fF8NOCpxEGs0OYA/exec"

LOGO_PATH = "assets/images/logo.png"

ADMIN_PASSWORD = "HgM18082019$&)"

COMPANY_PHONE = "01286609535"


# =========================
# SHEETS
# =========================

SHEETS = {
    "Customers": "0",
    "Maintenance": "2120582392",
    "Inventory": "1767710106",
    "Expenses": "288947510",
    "Store_Products": "1129472026",
}


# =========================
# HELPERS
# =========================

def to_num(x):
    try:
        return float(str(x).replace(",", "")) if x not in ["", None] else 0
    except:
        return 0


def load_data(gid):
    url = f"https://docs.google.com/spreadsheets/d/1RGDGJaP_lo2Fp2beLqAQvLulqMk2WDJKqLv2g34-ycc/export?format=csv&gid={gid}"
    try:
        df = pd.read_csv(url)
        df.columns = [str(c).strip() for c in df.columns]
        return df.fillna("")
    except:
        return pd.DataFrame()


def call_api(action, sheet, data=None, row_index=None):
    payload = {
        "action": action,
        "sheet": sheet,
        "data": data,
        "row_index": row_index
    }
    try:
        r = requests.post(WEB_APP_URL, json=payload, timeout=20)
        return r.status_code == 200
    except:
        return False


# =========================
# SESSION
# =========================

if "user_type" not in st.session_state:
    st.session_state.user_type = None


# =========================
# LOAD DATA
# =========================

df_c = load_data(SHEETS["Customers"])
df_m = load_data(SHEETS["Maintenance"])
df_inv = load_data(SHEETS["Inventory"])
df_exp = load_data(SHEETS["Expenses"])
df_store = load_data(SHEETS["Store_Products"])


# =========================
# LOGIN
# =========================

if st.session_state.user_type is None:

    st.title("🚰 Healthy Water System")

    tab1, tab2 = st.tabs(["Admin", "Customer"])

    with tab1:
        pwd = st.text_input("Password", type="password")
        if st.button("Login"):
            if pwd == ADMIN_PASSWORD:
                st.session_state.user_type = "admin"
                st.rerun()
            else:
                st.error("Wrong password")

    with tab2:
        phone = st.text_input("Phone")
        if st.button("Enter"):
            if phone:
                st.session_state.user_type = "customer"
                st.session_state.phone = phone
                st.rerun()


# =========================
# ADMIN PANEL
# =========================

elif st.session_state.user_type == "admin":

    st.sidebar.image(LOGO_PATH, use_container_width=True)

    page = st.sidebar.selectbox(
        "Menu",
        ["Dashboard", "Customers", "Maintenance", "Inventory", "Expenses", "Store"]
    )

    # -------------------------
    # DASHBOARD
    # -------------------------
    if page == "Dashboard":
        st.title("📊 Dashboard")

    # -------------------------
    # CUSTOMERS (FIXED + CLEAN)
    # -------------------------
    elif page == "Customers":
        st.title("👥 Customer Profiles")

        # =========================
        # LOAD & PREPARE
        # =========================
        df = df_c.copy()

        if "area" in df.columns:
            df = df.sort_values(by="area")

        search = st.text_input("🔍 Search customer")

        if search:
            df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]

        st.markdown("---")

        # =========================
        # ADD NEW CUSTOMER
        # =========================
        with st.expander("➕ Add New Customer"):
            with st.form("add_customer_form"):

                name = st.text_input("Name")
                phone = st.text_input("Phone")
                phone1 = st.text_input("Phone 1")
                phone2 = st.text_input("Phone 2")
                phone3 = st.text_input("Phone 3")
                phone4 = st.text_input("Phone 4")

                address = st.text_input("Address")
                area = st.text_input("Area")
                location_url = st.text_input("Location URL (Google Maps)")
                install_date = st.date_input("Install Date")
                cycle = st.text_input("Cycle")
                status = st.text_input("Status")

                submitted = st.form_submit_button("💾 Save Customer")

                if submitted and name:
                    new_row = [
                        name, phone, phone1, phone2, phone3, phone4,
                        address, area, location_url,
                        str(install_date), cycle, status
                    ]

                    ok = call_api("append", "Customers", new_row)

                    if ok:
                        st.success("Customer added successfully")
                        st.rerun()
                    else:
                        st.error("Failed to add customer")

        st.markdown("---")

        # =========================
        # DISPLAY CUSTOMERS
        # =========================
        for i, row in df.iterrows():

            row_id = row.get("row_index", i + 2)  # fallback مهم

            with st.expander(f"👤 {row.get('name','')} | 📍 {row.get('area','')}"):

                # -------------------------
                # PHONES (FIX: no None buttons)
                # -------------------------
                phones = [
                    row.get("phone"),
                    row.get("phone_1"),
                    row.get("phone_2"),
                    row.get("phone_3"),
                    row.get("phone_4"),
                ]

                st.write("📞 Phones:")

                for idx, ph in enumerate(phones):
                    if ph and str(ph).strip().lower() != "none":

                        c1, c2 = st.columns([1, 2])
                        c1.write(ph)

                        c2.markdown(
                            f"""
                            [📞 Call](tel:{ph}) |
                            [💬 WhatsApp](https://wa.me/2{ph})
                            """
                        )

                # -------------------------
                # INFO
                # -------------------------
                st.write(f"🏠 Address: {row.get('adress','')}")
                st.write(f"📍 Area: {row.get('area','')}")
                st.write(f"📅 Install: {row.get('install_date','')}")
                st.write(f"🔁 Cycle: {row.get('cycle','')}")
                st.write(f"📌 Status: {row.get('status','')}")

                # -------------------------
                # LOCATION (FIX)
                # -------------------------
                loc = row.get("location_url", "")
                if loc and str(loc).strip().lower() != "none":
                    st.markdown(f"📍 [Open Location in Maps]({loc})")

                st.markdown("---")

                # =========================
                # EDIT CUSTOMER
                # =========================
                if st.button("✏️ Edit", key=f"edit_{row_id}"):

                    st.session_state.editing = row_id

                if st.session_state.get("editing") == row_id:

                    with st.form(f"edit_form_{row_id}"):

                        ename = st.text_input("Name", row.get("name",""))
                        ephone = st.text_input("Phone", row.get("phone",""))
                        ephone1 = st.text_input("Phone 1", row.get("phone_1",""))
                        ephone2 = st.text_input("Phone 2", row.get("phone_2",""))
                        ephone3 = st.text_input("Phone 3", row.get("phone_3",""))
                        ephone4 = st.text_input("Phone 4", row.get("phone_4",""))

                        eaddress = st.text_input("Address", row.get("adress",""))
                        earea = st.text_input("Area", row.get("area",""))
                        elocation = st.text_input("Location URL", row.get("location_url",""))
                        ecycle = st.text_input("Cycle", row.get("cycle",""))
                        estatus = st.text_input("Status", row.get("status",""))

                        save_edit = st.form_submit_button("💾 Update")
    
                        if save_edit:

                            updated = [
                                ename, ephone, ephone1, ephone2, ephone3, ephone4,
                                eaddress, earea, elocation,
                                row.get("install_date",""),
                                ecycle, estatus
                            ]

                            ok = call_api("update", "Customers", updated, row_id)

                            if ok:
                                st.success("Updated successfully")
                                st.session_state.editing = None
                                st.rerun()
                            else:
                                st.error("Update failed")

                # =========================
                # DELETE CUSTOMER (FIX)
                # =========================
                if st.button("🗑️ Delete", key=f"del_{row_id}"):

                    ok = call_api("delete", "Customers", row_index=row_id)

                    if ok:
                        st.success("Deleted successfully")
                        st.rerun()
                    else:
                        st.error("Delete failed")
    # -------------------------
    # MAINTENANCE
    # -------------------------
    elif page == "Maintenance":
        st.title("🔧 Maintenance")
        st.dataframe(df_m)

    # -------------------------
    # INVENTORY
    # -------------------------
    elif page == "Inventory":
        st.title("📦 Inventory")
        st.dataframe(df_inv)

    # -------------------------
    # EXPENSES
    # -------------------------
    elif page == "Expenses":
        st.title("💵 Expenses")
        st.dataframe(df_exp)

    # -------------------------
    # STORE
    # -------------------------
    elif page == "Store":
        st.title("🛒 Store")
        st.dataframe(df_store)


# =========================
# CUSTOMER PANEL
# =========================

elif st.session_state.user_type == "customer":

    st.sidebar.image(LOGO_PATH, use_container_width=True)

    st.title("👤 My Account")

    phone = st.session_state.get("phone")

    if phone:

        user = df_c[df_c["phone"].astype(str) == str(phone)]

        st.subheader("📄 My Data")
        st.dataframe(user)

        names = user["name"].tolist() if "name" in user.columns else []

        history = df_m[df_m["name"].isin(names)]

        st.subheader("🔧 Maintenance History")
        st.dataframe(history)

        st.markdown("### 📞 Contact")
        st.markdown(f"""
        ☎️ {COMPANY_PHONE}  
        [Call](tel:{COMPANY_PHONE}) | 
        [WhatsApp](https://wa.me/2{COMPANY_PHONE})
        """)
