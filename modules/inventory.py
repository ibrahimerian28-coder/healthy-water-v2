import streamlit as st
import pandas as pd
from utils.data_service import load_sheet
from datetime import datetime

def app():

    st.title("📦 Inventory")

    gid = st.session_state.SHEETS["Inventory"]
    df = load_sheet(gid)
    # =========================
    # Inventory Statistics
    # =========================
    
    df["quantity"] = pd.to_numeric(
        df["quantity"],
        errors="coerce"
    ).fillna(0)
    
    df["min_limit"] = pd.to_numeric(
        df["min_limit"],
        errors="coerce"
    ).fillna(0)
    
    df["cost_price"] = pd.to_numeric(
        df["cost_price"],
        errors="coerce"
    ).fillna(0)
    
    total_items = len(df)
    
    low_stock = len(
        df[
            df["quantity"] <= df["min_limit"]
        ]
    )
    
    total_quantity = int(
        df["quantity"].sum()
    )
    
    inventory_value = (
        df["quantity"] *
        df["cost_price"]
    ).sum()
    
    c1, c2, c3, c4 = st.columns(4)
    
    c1.metric(
        "📦 الأصناف",
        total_items
    )
    
    c2.metric(
        "⚠️ منخفض المخزون",
        low_stock
    )
    
    c3.metric(
        "📊 إجمالي الكميات",
        total_quantity
    )
    
    c4.metric(
        "💰 قيمة المخزون",
        f"{inventory_value:,.0f} ج.م"
    )
    
    st.divider()

    history_gid = st.session_state.SHEETS["Inventory_History"]
    df_history = load_sheet(history_gid)
    
    if "date" in df_history.columns:
        df_history["date"] = df_history["date"].astype(str)
    
    st.write("عدد الأصناف:", len(df))
    
    for _, row in df.iterrows():
        qty = int(pd.to_numeric(row["quantity"], errors="coerce") or 0)
        min_qty = int(pd.to_numeric(row["min_limit"], errors="coerce") or 0)
        
        if qty < min_qty:
            card_color = "#ffe5e5"
            status_icon = "🔴"
        
        elif qty == min_qty:
            card_color = "#fff8d9"
            status_icon = "🟡"
        
        else:
            card_color = "#e8ffe8"
            status_icon = "🟢"
    
       with st.container(border=True):

           st.markdown(
               f"""
       <div style="
       background:{card_color};
       padding:12px;
       border-radius:10px;
       margin-bottom:10px;
       ">
       """,
               unsafe_allow_html=True
           )
    
           col1, col2, col3 = st.columns([4,2,2])
    
           with col1:
               st.markdown(
                   f"### {status_icon} {row['item_name']}"
               )
    
            with col2:
                st.metric(
                    "الكمية",
                    row["quantity"]
                )
    
            with col3:
    
                show = st.button(
                    "📜 History",
                    key=f"history_{row['item_name']}"
                )
    
            if show:
    
                history = df_history[
                    df_history["item_name"]
                    .astype(str)
                    .str.strip()
                    .str.lower()
                    ==
                    str(row["item_name"])
                    .strip()
                    .lower()
                ]
    
                if history.empty:
    
                    st.info("لا توجد حركات لهذا الصنف")
    
                else:
    
                    history = history.sort_values(
                        "date",
                        ascending=False
                    )
                    
                    for _, h in history.iterrows():
                    
                        movement = str(h.get("movement", "")).upper()
                    
                        if movement == "OUT":
                            color = "#ffe5e5"
                            title = "🟥 خصم من المخزون"
                    
                        elif movement == "IN":
                            color = "#e8ffe8"
                            title = "🟩 إضافة للمخزون"
                    
                        else:
                            color = "#fff8d9"
                            title = "🟨 تعديل بالمخزون"
                    
                        date = str(h.get("date", ""))[:10]
                    
                        with st.expander(
                            f"{title} | {h.get('item_name','')} | {date}"
                        ):
                    
                            st.markdown(
                                f"""
                    <div style="
                    background:{color};
                    padding:12px;
                    border-radius:10px;
                    ">
                    
                                        
                    <b>📅 التاريخ:</b> {date}<br>
                    
                    <b>📦 الصنف:</b> {h.get("item_name","")}<br>
                    
                    <b>🔢 الكمية:</b> {h.get("quantity","")}<br>
                    
                    <b>👨‍🔧 الفني:</b> {h.get("technician","")}<br>
                    
                    <b>🔗 المرجع:</b> {h.get("reference","")}<br>
                    
                    <b>📝 الملاحظات:</b> {h.get("notes","")}
                    
                    </div>
                    """,
                                unsafe_allow_html=True
                            )
