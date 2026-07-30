import streamlit as st
from utils.data_service import load_sheet
from datetime import datetime

def app():

    st.title("📦 Inventory")

    gid = st.session_state.SHEETS["Inventory"]
    df = load_sheet(gid)

    history_gid = st.session_state.SHEETS["Inventory_History"]
    df_history = load_sheet(history_gid)
    
    if "date" in df_history.columns:
        df_history["date"] = df_history["date"].astype(str)
    
    st.write("عدد الأصناف:", len(df))
    
    for _, row in df.iterrows():
    
        with st.container(border=True):
    
            col1, col2, col3 = st.columns([4,2,2])
    
            with col1:
                st.markdown(f"### 📦 {row['item_name']}")
    
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
