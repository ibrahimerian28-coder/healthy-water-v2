import streamlit as st
import pandas as pd

st.title("📊 Dashboard - Healthy Water")

col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 العملاء", len(df_c))
col2.metric("🔧 الصيانات", len(df_m))
col3.metric("💰 الإيراد", f"{total_revenue} ج.م")
col4.metric("📦 مخزون منخفض", low_stock_items)

st.divider()
st.subheader("🏆 أفضل العملاء ربحًا")
st.subheader("📅 الإيراد الشهري")
st.subheader("📊 KPI Dashboard")
st.subheader("🚨 تنبيه المخزون")

# =========================
# 🔐 Safe Loader (مهم جدًا)
# =========================
def safe_read(url):
    try:
        return pd.read_csv(url)
    except:
        return pd.DataFrame()

# =========================
# 👥 Customers
# =========================
df_c = safe_read(
    "https://docs.google.com/spreadsheets/d/15jfgmIYddNQvzieuVTtepNSmvKcEsD5PqUMMatYyVlQ/export?format=csv&gid=0"
)
total_customers = len(df_c)

# =========================
# 🔧 Maintenance
# =========================
df_m = safe_read(
    "https://docs.google.com/spreadsheets/d/15jfgmIYddNQvzieuVTtepNSmvKcEsD5PqUMMatYyVlQ/export?format=csv&gid=2120582392"
)

total_maintenance = len(df_m)

if "amount" in df_m.columns:
    df_m["amount"] = pd.to_numeric(df_m["amount"], errors="coerce").fillna(0)
    total_revenue = df_m["amount"].sum()
else:
    total_revenue = 0

# =========================
# 📦 Inventory
# =========================
df_inv = safe_read(
    "https://docs.google.com/spreadsheets/d/15jfgmIYddNQvzieuVTtepNSmvKcEsD5PqUMMatYyVlQ/export?format=csv&gid=1767710106"
)

if "quantity" in df_inv.columns and "min_limit" in df_inv.columns:
    low_stock_items = len(df_inv[df_inv["quantity"] <= df_inv["min_limit"]])
else:
    low_stock_items = 0

# =========================
# 💵 Expenses
# =========================
df_exp = safe_read(
    "https://docs.google.com/spreadsheets/d/15jfgmIYddNQvzieuVTtepNSmvKcEsD5PqUMMatYyVlQ/export?format=csv&gid=288947510"
)

# =========================
# 🛒 Store Products
# =========================
df_store = safe_read(
    "https://docs.google.com/spreadsheets/d/15jfgmIYddNQvzieuVTtepNSmvKcEsD5PqUMMatYyVlQ/export?format=csv&gid=1129472026"
)

# =========================
# 📦 Orders
# =========================
df_orders = safe_read(
    "https://docs.google.com/spreadsheets/d/15jfgmIYddNQvzieuVTtepNSmvKcEsD5PqUMMatYyVlQ/export?format=csv&gid=1423854754"
)

# =========================
# 📊 Metrics UI
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 العملاء", total_customers)
col2.metric("🔧 الصيانات", total_maintenance)
col3.metric("💰 الإيراد", f"{total_revenue} ج.م")
col4.metric("📦 مخزون منخفض", low_stock_items)

st.divider()

# =========================
# 📈 Overview
# =========================
st.subheader("📈 نظرة عامة")

st.write("📌 عدد الطلبات:", len(df_orders))
st.write("📌 عدد المنتجات:", len(df_store))
st.write("📌 عدد المصروفات:", len(df_exp))

st.success("تم ربط كل الشيتات بنجاح ✔")
st.divider()
st.subheader("📈 الإيراد من الصيانات")

if not df_m.empty and "amount" in df_m.columns:
    df_m["amount"] = pd.to_numeric(df_m["amount"], errors="coerce").fillna(0)
    daily = df_m.groupby(df_m.index)["amount"].sum()

    st.line_chart(daily)
else:
    st.info("لا توجد بيانات لعرضها")
    st.subheader("👥 العملاء مقابل الصيانات")

col_chart1, col_chart2 = st.columns(2)

col_chart1.metric("عدد العملاء", len(df_c))
col_chart2.metric("عدد الصيانات", len(df_m))
st.subheader("📦 حالة المخزون")

if not df_inv.empty:
    if "quantity" in df_inv.columns and "item_name" in df_inv.columns:
        st.bar_chart(df_inv.set_index("item_name")["quantity"])
else:
    st.info("لا توجد بيانات مخزون")
