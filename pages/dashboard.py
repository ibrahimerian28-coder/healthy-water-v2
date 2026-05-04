import streamlit as st
import pandas as pd

# =========================
# 🔐 Config
# =========================
BASE_URL = "https://docs.google.com/spreadsheets/d/1RGDGJaP_lo2Fp2beLqAQvLulqMk2WDJKqLv2g34-ycc/export?format=csv&gid="

def safe_read(url):
    try:
        return pd.read_csv(url)
    except:
        return pd.DataFrame()

# =========================
# 📥 Load Data
# =========================
df_c = safe_read(BASE_URL + "0")
df_m = safe_read(BASE_URL + "2120582392")
df_inv = safe_read(BASE_URL + "1767710106")
df_exp = safe_read(BASE_URL + "288947510")
df_store = safe_read(BASE_URL + "1129472026")
df_orders = safe_read(BASE_URL + "1423854754")

# =========================
# 🧹 Clean Columns
# =========================
for df in [df_c, df_m, df_inv, df_exp, df_store, df_orders]:
    df.columns = df.columns.str.strip()

# =========================
# 📊 Calculations
# =========================

total_customers = len(df_c)
total_maintenance = len(df_m)

# Revenue
if not df_m.empty and "amount" in df_m.columns:
    df_m["amount"] = pd.to_numeric(df_m["amount"], errors="coerce").fillna(0)
    total_revenue = df_m["amount"].sum()
else:
    total_revenue = 0

# Low stock
if not df_inv.empty and "quantity" in df_inv.columns and "min_limit" in df_inv.columns:
    df_inv["quantity"] = pd.to_numeric(df_inv["quantity"], errors="coerce").fillna(0)
    df_inv["min_limit"] = pd.to_numeric(df_inv["min_limit"], errors="coerce").fillna(0)
    low_stock_items = len(df_inv[df_inv["quantity"] <= df_inv["min_limit"]])
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

st.write("📌 الطلبات:", len(df_orders))
st.write("📌 المنتجات:", len(df_store))
st.write("📌 المصروفات:", len(df_exp))

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

if not df_inv.empty and "item_name" in df_inv.columns and "quantity" in df_inv.columns:
    st.bar_chart(df_inv.set_index("item_name")["quantity"])
else:
    st.info("لا توجد بيانات مخزون")

# =========================
# 🧠 Debug (اختياري وقت التطوير)
# =========================
with st.expander("🔍 Debug Data"):
    st.write("Customers:", df_c.columns.tolist())
    st.write("Maintenance:", df_m.columns.tolist())
    st.write("Inventory:", df_inv.columns.tolist())
    st.write("Store:", df_store.columns.tolist())
