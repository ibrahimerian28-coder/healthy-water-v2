import streamlit as st
import pandas as pd

st.title("📊 Dashboard - Healthy Water")

# =========================
# 🔐 Loader
# =========================
def safe_read(url):
    try:
        return pd.read_csv(url)
    except:
        return pd.DataFrame()

# =========================
# 📥 Load Data (مرة واحدة فقط)
# =========================
df_c = safe_read("https://docs.google.com/spreadsheets/d/15jfgmIYddNQvzieuVTtepNSmvKcEsD5PqUMMatYyVlQ/export?format=csv&gid=0")

df_m = safe_read("https://docs.google.com/spreadsheets/d/15jfgmIYddNQvzieuVTtepNSmvKcEsD5PqUMMatYyVlQ/export?format=csv&gid=2120582392")

df_inv = safe_read("https://docs.google.com/spreadsheets/d/15jfgmIYddNQvzieuVTtepNSmvKcEsD5PqUMMatYyVlQ/export?format=csv&gid=1767710106")

df_exp = safe_read("https://docs.google.com/spreadsheets/d/15jfgmIYddNQvzieuVTtepNSmvKcEsD5PqUMMatYyVlQ/export?format=csv&gid=288947510")

df_store = safe_read("https://docs.google.com/spreadsheets/d/15jfgmIYddNQvzieuVTtepNSmvKcEsD5PqUMMatYyVlQ/export?format=csv&gid=1129472026")

df_orders = safe_read("https://docs.google.com/spreadsheets/d/15jfgmIYddNQvzieuVTtepNSmvKcEsD5PqUMMatYyVlQ/export?format=csv&gid=1423854754")

# =========================
# 📊 Calculations
# =========================
total_customers = len(df_c)
total_maintenance = len(df_m)

if "amount" in df_m.columns:
    df_m["amount"] = pd.to_numeric(df_m["amount"], errors="coerce").fillna(0)
    total_revenue = df_m["amount"].sum()
else:
    total_revenue = 0

if "quantity" in df_inv.columns and "min_limit" in df_inv.columns:
    low_stock_items = len(df_inv[df_inv["quantity"] <= df_inv["min_limit"]])
else:
    low_stock_items = 0

# =========================
# 📊 UI (هنا بس العرض)
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 العملاء", total_customers)
col2.metric("🔧 الصيانات", total_maintenance)
col3.metric("💰 الإيراد", f"{total_revenue} ج.م")
col4.metric("📦 مخزون منخفض", low_stock_items)

st.divider()

st.subheader("📈 نظرة عامة")
st.write("📌 الطلبات:", len(df_orders))
st.write("📌 المنتجات:", len(df_store))
st.write("📌 المصروفات:", len(df_exp))

st.success("تم ربط البيانات بنجاح ✔")

# =========================
# 📊 Charts
# =========================
st.divider()
st.subheader("📈 الإيراد من الصيانات")

if not df_m.empty and "amount" in df_m.columns:
    st.line_chart(df_m["amount"])
else:
    st.info("لا توجد بيانات")

st.subheader("📦 المخزون")

if not df_inv.empty and "item_name" in df_inv.columns:
    st.bar_chart(df_inv.set_index("item_name")["quantity"])
