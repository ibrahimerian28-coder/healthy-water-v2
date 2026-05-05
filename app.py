import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# =========================
# 🔥 CONFIG
# =========================

st.set_page_config(page_title="Healthy Water Pro", layout="wide")

WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwPIG6-S1aOxIL5KvN-XF_zwW0Xu6U9ARLau_R21s_Z9MJafWuPZW8fF8NOCpxEGs0OYA/exec"

LOGO_PATH = "assets/images/logo.png"

ADMIN_PASSWORD = "HgM18082019$&)"

COMPANY_PHONE = "01286609535"


# =========================
# 🔥 SHEETS GIDs
# =========================

SHEETS = {
    "Customers": "0",
    "Maintenance": "2120582392",
    "Inventory": "1767710106",
    "Expenses": "288947510",
    "Store_Products": "1129472026",
}


# =========================
# 🔥 HELPERS
# =========================

def to_num(v):
    try:
        return float(str(v).replace(",", "")) if v not in [None, ""] else 0
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


def execute_gsheet_action(action, sheet, data=None, row_index=None):
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
# 🔥 SESSION STATE
# =========================

if "user_type" not in st.session_state:
    st.session_state.user_type = None


# =========================
# 🔥 LOAD DATA
# =========================

df_c = load_data(SHEETS["Customers"])
df_m = load_data(SHEETS["Maintenance"])
df_inv = load_data(SHEETS["Inventory"])
df_exp = load_data(SHEETS["Expenses"])
df_store = load_data(SHEETS["Store_Products"])


# =========================
# 🔐 LOGIN PAGE
# =========================

if st.session_state.user_type is None:

    st.title("🚰 Healthy Water System")

    tab1, tab2 = st.tabs(["🔒 Admin", "👤 Customer"])

    with tab1:
        pwd = st.text_input("Password", type="password")
        if st.button("Login Admin"):
            if pwd == ADMIN_PASSWORD:
                st.session_state.user_type = "admin"
                st.rerun()
            else:
                st.error("Wrong password")

    with tab2:
        phone = st.text_input("Phone Number")
        if st.button("Login Customer"):
            if phone.strip() != "":
                st.session_state.user_type = "customer"
                st.session_state.phone = phone
                st.rerun()


# =========================
# 👑 ADMIN PANEL
# =========================

elif st.session_state.user_type == "admin":

    st.sidebar.image(LOGO_PATH, use_container_width=True)

    page = st.sidebar.selectbox(
        "📌 Menu",
        [
            "Dashboard",
            "Customers",
            "Maintenance",
            "Inventory",
            "Expenses",
            "Store"
        ]
    )

    # -------------------------
    # DASHBOARD
    # -------------------------
    if page == "Dashboard":
        st.title("📊 Dashboard")

    # -------------------------
    # CUSTOMERS
    # -------------------------
    elif page == "Customers":
        st.title("👥 Customers")

        search = st.text_input("Search")
        if search:
            df_show = df_c[df_c.astype(str).apply(lambda x: x.str.contains(search, case=False)).any(axis=1)]
        else:
            df_show = df_c

        st.dataframe(df_show, use_container_width=True)

    # -------------------------
    # MAINTENANCE
    # -------------------------
    elif page == "Maintenance":
        st.title("🔧 Maintenance")

        st.dataframe(df_m, use_container_width=True)

    # -------------------------
    # INVENTORY
    # -------------------------
    elif page == "Inventory":
        st.title("📦 Inventory")

        st.dataframe(df_inv, use_container_width=True)

    # -------------------------
    # EXPENSES
    # -------------------------
    elif page == "Expenses":
        st.title("💵 Expenses")

        st.dataframe(df_exp, use_container_width=True)

    # -------------------------
    # STORE
    # -------------------------
    elif page == "Store":
        st.title("🛒 Store Products")

        st.dataframe(df_store, use_container_width=True)


# =========================
# 👤 CUSTOMER PANEL
# =========================

elif st.session_state.user_type == "customer":

    st.sidebar.image(LOGO_PATH, use_container_width=True)

    st.title("👤 Customer Area")

    phone = st.session_state.get("phone")

    if phone:
        user_data = df_c[df_c["phone"].astype(str) == str(phone)]

        st.subheader("📄 Your Data")
        st.dataframe(user_data)

        st.subheader("🔧 Your Maintenance History")

        cust_names = user_data["name"].tolist() if "name" in user_data.columns else []
        df_hist = df_m[df_m["name"].isin(cust_names)]

        st.dataframe(df_hist)

        st.markdown("### 📞 Contact Us")
        st.markdown(f"""
        ☎️ {COMPANY_PHONE}  
        [Call](tel:{COMPANY_PHONE}) | 
        [WhatsApp](https://wa.me/2{COMPANY_PHONE})
        """)
