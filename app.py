import streamlit as st
import pandas as pd
import requests
import base64
import os
from datetime import datetime, timedelta
import plotly.express as px
import urllib.parse

# =========================
# ⚙️ CONFIG (لازم أول سطر فعلي بعد الاستيراد)
# =========================
st.set_page_config(page_title="Healthy Water Pro", layout="wide", page_icon="🚰")

# =========================
# 🔐 SESSION STATE
# =========================
if "user_type" not in st.session_state:
    st.session_state.user_type = None

if "customer_data" not in st.session_state:
    st.session_state.customer_data = None

if "cart" not in st.session_state:
    st.session_state.cart = []

# =========================
# 🔥 SETTINGS
# =========================
BASE_URL = "https://docs.google.com/spreadsheets/d/1RGDGJaP_lo2Fp2beLqAQvLulqMk2WDJKqLv2g34-ycc/export?format=csv&gid="
WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwS0CSCFl0fSQyvefV8X1mn2YaNQ044F6KpFG8XMJsyhcT4VcaeCfPKBtG2dP74mgsq/exec"

COMPANY_PHONE = "01286609535"

ADMIN_PASSWORD = st.secrets.get("ADMIN_PASSWORD", "1234")

LOGO_PATH = "assets/images/logo.png"


# =========================
# 📊 DATA LOADER (مهم جدًا)
# =========================
@st.cache_data(ttl=5)
def load_data(gid):
    try:
        url = f"{BASE_URL}{gid}"
        df = pd.read_csv(url)
        df.columns = [str(c).strip() for c in df.columns]
        return df.fillna("")
    except:
        return pd.DataFrame()


# =========================
# 🔧 SAFE NUMBER
# =========================
def to_num(val):
    try:
        return int(float(str(val).replace(",", "")))
    except:
        return 0


# =========================
# 📡 GOOGLE SHEETS ACTION
# =========================
def execute_gsheet_action(action, sheet_name, data=None, row_index=None):
    payload = {
        "action": action,
        "sheet": sheet_name,
        "data": data,
        "row_index": row_index
    }
    try:
        r = requests.post(WEB_APP_URL, json=payload, timeout=15)
        return r.status_code == 200
    except:
        return False


# =========================
# 📦 LOAD DATASETS
# =========================
df_c = df_m = df_inv = df_exp = df_store = pd.DataFrame()
df_orders = pd.DataFrame()  # مهم عشان مايحصلش NameError

if st.session_state.user_type:
    df_c = load_data("0")
    df_m = load_data("2120582392")
    df_inv = load_data("1767710106")
    df_exp = load_data("288947510")
    df_store = load_data("1168172935")


# =========================
# 🔐 LOGIN PAGE
# =========================
if st.session_state.user_type:
    st.session_state.df_c = load_data("0")
    st.session_state.df_m = load_data("2120582392")
    st.session_state.df_inv = load_data("1767710106")
    st.session_state.df_exp = load_data("288947510")
    st.session_state.df_store = load_data("1168172935")
else:
    st.session_state.df_c = pd.DataFrame()
    st.session_state.df_m = pd.DataFrame()
    st.session_state.df_inv = pd.DataFrame()
    st.session_state.df_exp = pd.DataFrame()
    st.session_state.df_store = pd.DataFrame()


# =========================
# 🔥 NAVIGATION
# =========================
page = st.sidebar.selectbox(
    "📌 القائمة",
    ["Dashboard", "Customers", "Maintenance", "Inventory", "Store"]
)


# =========================
# 📊 DASHBOARD
# =========================
if page == "Dashboard":
    st.title("📊 Dashboard")

    col1, col2, col3 = st.columns(3)
    col1.metric("👥 العملاء", len(df_c))
    col2.metric("🔧 الصيانات", len(df_m))
    col3.metric("📦 المنتجات", len(df_store))

    st.divider()

    st.write("📌 الطلبات:", len(df_orders))
    st.write("📌 المصروفات:", len(df_exp))


# =========================
# 👥 CUSTOMERS (مبدئي)
# =========================
elif page == "Customers":
    st.title("👥 Customers")
    st.dataframe(df_c)


# =========================
# 🔧 MAINTENANCE
# =========================
elif page == "Maintenance":
    st.title("🔧 Maintenance")
    st.dataframe(df_m)


# =========================
# 📦 INVENTORY
# =========================
elif page == "Inventory":
    st.title("📦 Inventory")
    st.dataframe(df_inv)


# =========================
# 🛒 STORE (مختصر لتجنب التعقيد)
# =========================
elif page == "Store":
    st.title("🛒 Store")
    st.dataframe(df_store)
