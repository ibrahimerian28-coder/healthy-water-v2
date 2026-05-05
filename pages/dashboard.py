import streamlit as st
import pandas as pd

st.title("📊 Dashboard - Healthy Water")

# =========================
# 📦 جلب البيانات من session_state
# =========================
df_c = st.session_state.get("df_c", pd.DataFrame())
df_m = st.session_state.get("df_m", pd.DataFrame())
df_inv = st.session_state.get("df_inv", pd.DataFrame())
df_exp = st.session_state.get("df_exp", pd.DataFrame())
df_store = st.session_state.get("df_store", pd.DataFrame())

# =========================
# 🚨 حماية
# =========================
if df_c.empty and df_m.empty:
    st.warning("⚠️ لازم تسجل دخول كأدمن الأول")
    st.stop()

# =========================
# 📊 Metrics
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 العملاء", len(df_c))
col2.metric("🔧 الصيانات", len(df_m))
col3.metric("📦 المنتجات", len(df_store))
col4.metric("💰 المصروفات", len(df_exp))

st.divider()

# =========================
# 📌 Overview
# =========================
st.subheader("📈 نظرة عامة")

st.write("👥 العملاء:", len(df_c))
st.write("🔧 الصيانات:", len(df_m))
st.write("📦 المنتجات:", len(df_store))
st.write("💰 المصروفات:", len(df_exp))

st.success("✔ البيانات متصلة بنجاح")
