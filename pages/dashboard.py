import streamlit as st
import pandas as pd

st.title("📊 Dashboard - Healthy Water")

# =========================
# 👥 Customers
# =========================
df_c = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/15jfgmIYddNQvzieuVTtepNSmvKcEsD5PqUMMatYyVlQ/export?format=csv&gid=0"
)
total_customers = len(df_c)

# =========================
# 🔧 Maintenance
# =========================
df_m = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/15jfgmIYddNQvzieuVTtepNSmvKcEsD5PqUMMatYyVlQ/export?format=csv&gid=2120582392"
)
total_maintenance = len(df_m)

df_m["amount"] = pd.to_numeric(df_m.get("amount", 0), errors="coerce").fillna(0)
total_revenue = df_m["amount"].sum()

# =========================
# 📦 Inventory
# =========================
df_inv = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/15jfgmIYddNQvzieuVTtepNSmvKcEsD5PqUMMatYyVlQ/export?format=csv&gid=1767710106"
)

if "quantity" in df_inv.columns and "min_limit" in df_inv.columns:
    low_stock_items = len(df_inv[df_inv["quantity"] <= df_inv["min_limit"]])
else:
    low_stock_items = 0

# =========================
# 📊 Expenses (موجودة لو حبيت تستخدمها لاحقًا)
# =========================
df_exp = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/15jfgmIYddNQvzieuVTtepNSmvKcEsD5PqUMMatYyVlQ/export?format=csv&gid=288947510"
)

# =========================
# 📊 Store (اختياري)
# =========================
df_store = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/15jfgmIYddNQvzieuVTtepNSmvKcEsD5PqUMMatYyVlQ/export?format=csv&gid=1129472026"
)

df_orders = pd.read_csv(
    "https://docs.google.com/spreadsheets/d/15jfgmIYddNQvzieuVTtepNSmvKcEsD5PqUMMatYyVlQ/export?format=csv&gid=1423854754"
)

# =========================
# 📊 عرض الإحصائيات
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 العملاء", total_customers)
col2.metric("🔧 الصيانات", total_maintenance)
col3.metric("💰 الإيراد", f"{total_revenue} ج.م")
col4.metric("📦 مخزون منخفض", low_stock_items)

st.divider()

st.subheader("📈 نظرة عامة")
st.success("تم ربط كل الشيتات بنجاح ✔")
