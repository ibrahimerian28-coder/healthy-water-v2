import streamlit as st

# =========================
# 📊 Dashboard Safe Version
# =========================

st.title("📊 Dashboard - Healthy Water")

# تأكد من وجود البيانات (Fallback آمن)
df_c = st.session_state.get("df_c", None)
df_m = st.session_state.get("df_m", None)
df_store = st.session_state.get("df_store", None)
df_exp = st.session_state.get("df_exp", None)

# لو البيانات مش متحمّلة
if df_c is None or df_m is None:
    st.warning("⚠️ برجاء تسجيل الدخول كأدمن لعرض البيانات")
    st.stop()

# تحويل None إلى DataFrame فاضي (حماية إضافية)
import pandas as pd

df_c = df_c if df_c is not None else pd.DataFrame()
df_m = df_m if df_m is not None else pd.DataFrame()
df_store = df_store if df_store is not None else pd.DataFrame()
df_exp = df_exp if df_exp is not None else pd.DataFrame()

# =========================
# 📌 Metrics
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 العملاء", len(df_c))
col2.metric("🔧 الصيانات", len(df_m))
col3.metric("📦 المنتجات", len(df_store))
col4.metric("💸 المصروفات", len(df_exp))

st.divider()

# =========================
# 📊 Overview
# =========================
st.subheader("📈 نظرة عامة")

st.write("📌 العملاء:", len(df_c))
st.write("📌 الصيانات:", len(df_m))
st.write("📌 المنتجات:", len(df_store))
st.write("📌 المصروفات:", len(df_exp))

st.success("✔ البيانات تعمل بشكل طبيعي")
