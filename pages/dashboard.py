import streamlit as st
import pandas as pd
from datetime import datetime

# هنا هنفترض إن الداتا بتتجاب من app أو api
st.title("📊 Dashboard - Healthy Water")

# أمثلة مؤقتة (لحد ما نربط الداتا الصح)
total_customers = 120
total_maintenance = 45
total_revenue = 25000
low_stock_items = 5

# عرض الإحصائيات
col1, col2, col3, col4 = st.columns(4)

col1.metric("👥 العملاء", total_customers)
col2.metric("🔧 الصيانات", total_maintenance)
col3.metric("💰 الإيراد", f"{total_revenue} ج.م")
col4.metric("📦 مخزون منخفض", low_stock_items)

st.divider()

st.subheader("📈 نظرة عامة")
st.info("هنا هنضيف الرسوم البيانية بعد ربط البيانات")
