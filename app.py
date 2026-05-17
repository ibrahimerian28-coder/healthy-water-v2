import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta
import uuid

# =========================
# CONFIG
# =========================

st.set_page_config(page_title="Healthy Water Pro", layout="wide")

APP_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzksKYGIuN41Pszdy3Bs_0UQa6kV9XV3lZe41o2_qmcSEAlcADF0TN0qcBhRXCYXjBc1A/exec"

WEB_APP_URL = APP_SCRIPT_URL

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

        # 👇 مهم جدًا: نقرأ رد السيرفر
        response_text = r.text.strip()

        st.write("DEBUG RESPONSE:", response_text)

        return response_text == "OK"

    except Exception as e:
        st.error(e)
        return False

# =========================
# SESSION
# =========================

if "user_type" not in st.session_state:
    st.session_state.user_type = None

st.session_state.APP_SCRIPT_URL = APP_SCRIPT_URL
st.session_state.SHEETS = SHEETS
st.session_state.COMPANY_PHONE = COMPANY_PHONE
st.session_state.LOGO_PATH = LOGO_PATH

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
# ADMIN PANEL ROUTER
# =========================

elif st.session_state.user_type == "admin":

    st.sidebar.image(LOGO_PATH, use_container_width=True)

    page = st.sidebar.selectbox(
        "Menu",
        ["Dashboard", "Customers", "Maintenance", "Inventory", "Expenses", "Store"]
    )

    if page == "Dashboard":
        import pages.dashboard as dashboard
        dashboard.app()

    elif page == "Customers":
        import pages.customers as customers
        customers.app()

    elif page == "Maintenance":
        import pages.maintenance as maintenance
        maintenance.app()

    elif page == "Inventory":
        import pages.inventory as inventory
        inventory.app()

    elif page == "Expenses":
        import pages.expenses as expenses
        expenses.app()

    elif page == "Store":
        import pages.store as store
        store.app()
