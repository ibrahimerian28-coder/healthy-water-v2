import streamlit as st
import pandas as pd
# تهيئة session state
if "user_type" not in st.session_state:
    st.session_state.user_type = None

if "customer_data" not in st.session_state:
    st.session_state.customer_data = None

# =========================
# 🔐 Config
# =========================
BASE_URL = "https://docs.google.com/spreadsheets/d/1RGDGJaP_lo2Fp2beLqAQvLulqMk2WDJKqLv2g34-ycc/export?format=csv&gid="

def safe_read(url):
    try:
        df = pd.read_csv(url)
        df.columns = [str(c).strip() for c in df.columns]
        return df
    except:
        return pd.DataFrame()

# =========================
if st.session_state.user_type is not None:
    df_c = load_data("0")
    df_m = load_data("2120582392")
    df_inv = load_data("1767710106")
    df_exp = load_data("288947510")
    df_store = load_data("1168172935")
else:
    df_c = pd.DataFrame()
    df_m = pd.DataFrame()
    df_inv = pd.DataFrame()
    df_exp = pd.DataFrame()
    df_store = pd.DataFrame()

# =========================
# 📊 Calculations
# =========================

# 👥 Customers
total_customers = len(df_c)

# 🔧 Maintenance
total_maintenance = len(df_m)

# 💰 Revenue (from Maintenance amount)
if not df_m.empty and "amount" in df_m.columns:
    df_m["amount"] = pd.to_numeric(df_m["amount"], errors="coerce").fillna(0)
    total_revenue = df_m["amount"].sum()
else:
    total_revenue = 0

# 📦 Inventory
if not df_inv.empty:
    if "quantity" in df_inv.columns:
        df_inv["quantity"] = pd.to_numeric(df_inv["quantity"], errors="coerce").fillna(0)
    if "min_limit" in df_inv.columns:
        df_inv["min_limit"] = pd.to_numeric(df_inv["min_limit"], errors="coerce").fillna(0)

    if "quantity" in df_inv.columns and "min_limit" in df_inv.columns:
        low_stock_items = len(df_inv[df_inv["quantity"] <= df_inv["min_limit"]])
    else:
        low_stock_items = 0
else:
    low_stock_items = 0

# =========================
# 🎯 UI
# =========================

st.title("📊 Dashboard - Healthy Water")

col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 العملاء", total_customers)
col2.metric("🔧 الصيانات", total_maintenance)
col3.metric("💰 الإيراد", f"{total_revenue} ج.م")
col4.metric("📦 مخزون منخفض", low_stock_items)

st.divider()

# =========================
# 📌 Overview
# =========================

st.subheader("📈 نظرة عامة")

st.write("📌 العملاء:", len(df_c))
st.write("📌 الصيانات:", len(df_m))
st.write("📌 المنتجات:", len(df_store))
st.write("📌 المصروفات:", len(df_exp))
st.write("📌 الطلبات:", len(df_orders))

st.success("تم ربط البيانات بنجاح ✔")

# =========================
# 📈 Charts
# =========================

st.divider()
st.subheader("📈 الإيراد من الصيانات")

if not df_m.empty and "amount" in df_m.columns:
    st.line_chart(df_m["amount"])
else:
    st.info("لا توجد بيانات للإيراد")

# =========================
# 📦 Inventory
# =========================

st.subheader("📦 المخزون")

if (
    not df_inv.empty
    and "item_name" in df_inv.columns
    and "quantity" in df_inv.columns
):
    st.bar_chart(df_inv.set_index("item_name")["quantity"])
else:
    st.info("لا توجد بيانات مخزون")

# =========================
# 🧠 Debug
# =========================

with st.expander("🔍 Debug Data"):
    st.write("Customers:", df_c.columns.tolist())
    st.write("Maintenance:", df_m.columns.tolist())
    st.write("Inventory:", df_inv.columns.tolist())
    st.write("Store:", df_store.columns.tolist())
    st.write("Expenses:", df_exp.columns.tolist())
