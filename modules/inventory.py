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

    numeric_columns = [
        "quantity",
        "min_limit",
        "cost_price",
        "ideal_stock"
    ]

    for col in numeric_columns:

        if col in df.columns:

            df[col] = pd.to_numeric(
                df[col],
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
        ideal_stock = int(row["ideal_stock"])
        cost_price = float(row["cost_price"])
        item_value = qty * cost_price

        if qty <= min_qty:

            status = "🔴 حرج"
        
            card_color = "#ffe5e5"
        
        elif ideal_stock > 0 and qty < ideal_stock * 0.5:
        
            status = "🟡 منخفض"
        
            card_color = "#fff8d9"
        
        else:
        
            status = "🟢 جيد"
        
            card_color = "#e8ffe8"

        with st.container(border=True):

            st.markdown(
                f"""
            <div style="
            background:{card_color};
            padding:18px;
            border-radius:14px;
            margin-bottom:12px;
            border-left:8px solid #2E86C1;
            ">
            
            <h3 style="
            margin:0;
            padding:0;
            ">
            📦 {row['item_name']}
            </h3>
            
            <div style="margin-top:10px;">

            <span style="
            padding:6px 14px;
            border-radius:20px;
            font-size:14px;
            font-weight:bold;
            color:white;
            
            background:
            {
            '#28a745'
            if 'جيد' in status
            else '#ffc107'
            if 'منخفض' in status
            else '#dc3545'
            };
            ">
            
            {status}
            
            </span>
            
            </div>
            """,
                unsafe_allow_html=True
            )

            c1, c2, c3, c4 = st.columns(
                [2, 2, 2, 2]
            )

            with c1:

                st.metric(
                    "📦 الكمية",
                    qty
                )

            with c2:

                st.metric(
                    "⚠️ الحد الأدنى",
                    min_qty
                )

            with c3:

                st.metric(
                    "💰 سعر الوحدة",
                    f"{cost_price:,.0f} ج.م"
                )

            with c4:

                show = st.button(
                    "📜 History",
                    key=f"history_{row['item_name']}",
                    use_container_width=True
                )
                st.metric(
                    "💵 قيمة الصنف",
                    f"{item_value:,.0f} ج.م"
                )

            # =========================
            # STOCK LEVEL
            # =========================

            if ideal_stock > 0:

                percent = min(
                    qty / ideal_stock,
                    1.0
                )

            else:

                percent = 1.0

            st.progress(percent)

            st.caption(
                f"المخزون الحالي : {qty} من {ideal_stock}"
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
                            icon = "➖"

                        elif movement == "IN":
                            title = "🟩 إضافة للمخزون"
                            bg = "#e8ffe8"
                            icon = "➕"

                        else:
                            title = "🟨 تعديل بالمخزون"
                            bg = "#fff8d9"
                            icon = "✏️"

                        date = str(
                            h.get("date", "")
                        )[:10]

                        technician = h.get(
                            "technician",
                            ""
                        )

                        reference = h.get(
                            "reference",
                            ""
                        )

                        notes = h.get(
                            "notes",
                            ""
                        )

                        quantity = h.get(
                            "quantity",
                            ""
                        )

                        with st.container(border=True):

                            st.markdown(
                                f"""
<div style="
background:{bg};
padding:14px;
border-radius:12px;
margin-bottom:8px;
">

### {icon} {title}

📅 **التاريخ:** {date}

📦 **الكمية:** {quantity}

👨‍🔧 **الفني:** {technician if technician else "-"}

🔗 **المرجع:** {reference if reference else "-"}

📝 **ملاحظات:** {notes if notes else "-"}

</div>
""",
                                unsafe_allow_html=True
                            )

                    st.divider()
