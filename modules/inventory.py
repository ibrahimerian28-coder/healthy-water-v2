import streamlit as st
import pandas as pd
from utils.data_service import load_sheet


def app():

    st.title("📦 Inventory")

    # =========================
    # LOAD DATA
    # =========================

    inventory_gid = st.session_state.SHEETS["Inventory"]
    history_gid = st.session_state.SHEETS["Inventory_History"]

    df = load_sheet(inventory_gid)
    df_history = load_sheet(history_gid)

    # =========================
    # CLEAN DATA
    # =========================

    df.columns = df.columns.str.strip()

    if not df_history.empty:
        df_history.columns = df_history.columns.str.strip()

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

    # =========================
    # DASHBOARD
    # =========================

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

    # =========================
    # INVENTORY CARDS
    # =========================

    for _, row in df.iterrows():

        qty = int(row["quantity"])
        min_qty = int(row["min_limit"])

        if qty < min_qty:
            status = "🔴"
            color = "#ffe5e5"

        elif qty == min_qty:
            status = "🟡"
            color = "#fff8d9"

        else:
            status = "🟢"
            color = "#e8ffe8"

        with st.container(border=True):

            c1, c2 = st.columns([5, 1])
        
            with c1:
        
                st.markdown(
                    f"""
        ### {status} {row['item_name']}
        
        📦 **الكمية الحالية:** {int(row['quantity'])}
        
        ⚠️ **الحد الأدنى:** {int(row['min_limit'])}
        
        💰 **سعر الشراء:** {row['cost_price']} ج.م
        """
                )
        
            with c2:
        
                show = st.button(
                    "📜 History",
                    key=f"history_{row['item_name']}",
                    use_container_width=True
                )

            
            # =========================
            # HISTORY
            # =========================

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

                        movement = str(
                            h.get("movement", "")
                        ).upper()

                        if movement == "OUT":
                            title = "🟥 خصم من المخزون"
                            bg = "#ffe5e5"

                        elif movement == "IN":
                            title = "🟩 إضافة للمخزون"
                            bg = "#e8ffe8"

                        else:
                            title = "🟨 تعديل بالمخزون"
                            bg = "#fff8d9"

                        date = str(
                            h.get("date", "")
                        )[:10]

                        with st.expander(
                            f"{title} | {date}"
                        ):

                            st.markdown(
                                f"""
<div style="
background:{bg};
padding:15px;
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
