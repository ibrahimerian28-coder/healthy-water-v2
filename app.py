import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta

# =========================
# CONFIG
# =========================

st.set_page_config(page_title="Healthy Water Pro", layout="wide")

WEB_APP_URL = "https://script.google.com/macros/s/AKfycbxMLqtxXhshfy7IWkbKOCnT5uT85yFQic9ZO8Kc8uOinGWGGkyIqr1PrSIuCUonKXh0LQ/exec"

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
    # CUSTOMERS (FULL CRUD FINAL)
    # -------------------------
    elif page == "Customers":

        st.title("👥 Customer Management")

        # =========================
        # HELPERS
        # =========================
        def clean_phone(p):
            if pd.isna(p):
                return ""
            p = str(p).strip()
            if p.lower() in ["none", "nan", ""]:
                return ""
            return p

        def wa_link(phone):
            phone = clean_phone(phone)
            phone = phone.replace(" ", "")
            if phone.startswith("0"):
                phone = "2" + phone
            return f"https://wa.me/{phone}"

        # =========================
        # LOAD + CLEAN DATA
        # =========================
        df = df_c.copy()
        df.columns = df.columns.str.strip()

        if "name" in df.columns:
            df = df[df["name"].astype(str).str.strip() != ""]

        df = df.reset_index(drop=True)

        # ترتيب حسب المنطقة
        if "area" in df.columns:
            df = df.sort_values(by="area", na_position="last")

        # =========================
        # ➕ ADD CUSTOMER
        # =========================
        with st.expander("➕ Add New Customer"):
            with st.form("add_customer"):

                name = st.text_input("Name")
                phone = st.text_input("Phone")
                phone1 = st.text_input("Phone 1")
                phone2 = st.text_input("Phone 2")
                phone3 = st.text_input("Phone 3")
                phone4 = st.text_input("Phone 4")

                address = st.text_input("Address")
                area = st.text_input("Area")
                location_url = st.text_input("Google Maps URL")
                install_date = st.text_input("Install Date")
                cycle = st.text_input("Cycle")
                status = st.text_input("Status", value="نشط")

                submit = st.form_submit_button("Save")

                if submit:
                    new_row = [
                        "",  # customer_id auto
                        name, phone, phone1, phone2, phone3, phone4,
                        address, area, location_url,
                        install_date, cycle, status
                    ]

                    ok = call_api("append", "Customers", new_row)

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
            df = df[df.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]

        st.write("عدد العملاء:", len(df))

        # =========================
        # DISPLAY CUSTOMERS
        # =========================
        for i in range(len(df)):

            row = df.iloc[i]

            name = str(row.get("name", "")).strip()
            if not name:
                continue

            area = str(row.get("area", "")).strip()
            customer_id = str(row.get("customer_id", f"row_{i}"))

            real_row_index = i + 2  # مهم للـ API

            with st.expander(f"👤 {name} | 📍 {area} | 🆔 {customer_id}"):

                # -------- phones --------
                st.write("📞 Phones:")

                phones = [
                    row.get("phone"),
                    row.get("phone_1"),
                    row.get("phone_2"),
                    row.get("phone_3"),
                    row.get("phone_4"),
                ]

                for ph in phones:
                    ph = clean_phone(ph)

                    if ph:
                        col1, col2 = st.columns([1, 3])
                        col1.write(ph)
                        col2.markdown(
                            f"[📞 Call](tel:{ph}) | [💬 WhatsApp]({wa_link(ph)})"
                        )

                # -------- details --------
                if row.get("address"):
                    st.write(f"🏠 {row.get('address')}")

                if row.get("install_date"):
                    st.write(f"📅 {row.get('install_date')}")

                if row.get("cycle"):
                    st.write(f"🔁 Cycle: {row.get('cycle')}")

                if row.get("status"):
                    st.write(f"📌 {row.get('status')}")

                # -------- location --------
                loc = str(row.get("location_url", "")).strip()
                if loc and loc.lower() != "nan":
                    if loc and loc.lower() != "nan":
                        fixed_loc = f"https://www.google.com/maps/search/?api=1&query={loc}"
                        st.markdown(f"[📍 Open Location in Maps]({fixed_loc})")

                st.divider()

                # ================= ACTIONS =================
                col1, col2 = st.columns(2)

                # 🗑 DELETE
                with col1:
                    if st.button("🗑️ Delete", key=f"del_{customer_id}_{i}"):

                        ok = call_api("delete", "Customers", row_index=real_row_index)

                        if ok:
                            st.success("Deleted")
                            st.rerun()
                        else:
                            st.error("Delete failed")

                # ✏️ EDIT
                with col2:
                    if st.button("✏️ Edit", key=f"edit_{customer_id}_{i}"):

                        st.session_state["edit_data"] = row.to_dict()
                        st.session_state["edit_index"] = real_row_index
                        st.rerun()

        # =========================
        # EDIT FORM
        # =========================
        if "edit_data" in st.session_state:

            st.divider()
            st.subheader("✏️ Edit Customer")

            er = st.session_state["edit_data"]
            rid = st.session_state["edit_index"]

            with st.form("edit_form"):

                name = st.text_input("Name", er.get("name",""))
                phone = st.text_input("Phone", er.get("phone",""))
                phone1 = st.text_input("Phone 1", er.get("phone_1",""))
                phone2 = st.text_input("Phone 2", er.get("phone_2",""))
                phone3 = st.text_input("Phone 3", er.get("phone_3",""))
                phone4 = st.text_input("Phone 4", er.get("phone_4",""))

                address = st.text_input("Address", er.get("address",""))
                area = st.text_input("Area", er.get("area",""))
                location_url = st.text_input("Location URL", er.get("location_url",""))
                install_date = st.text_input("Install Date", er.get("install_date",""))
                cycle = st.text_input("Cycle", er.get("cycle",""))
                status = st.text_input("Status", er.get("status",""))

                save = st.form_submit_button("Save Changes")

                if save:

                    updated = [
                        er.get("customer_id",""),
                        name, phone, phone1, phone2, phone3, phone4,
                        address, area, location_url,
                        install_date, cycle, status
                    ]

                    ok = call_api("update", "Customers", updated, row_index=rid)

                    if ok:
                        st.success("✅ Updated")
                        del st.session_state["edit_data"]
                        del st.session_state["edit_index"]
                        st.rerun()
                    else:
                        st.error("❌ Update failed")

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
