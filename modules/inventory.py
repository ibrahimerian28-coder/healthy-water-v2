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
        "📦 Items",
        total_items
    )

    c2.metric(
        "⚠️ Low Stock",
        low_stock
    )

    c3.metric(
        "📊 Total Quantity",
        total_quantity
    )

    c4.metric(
        "💰  Inventory Value",
        f"{inventory_value:,.0f} EGP"
    )

    st.divider()
    # =========================
    # SEARCH
    # =========================
    
    search = st.text_input(
        "🔍 Search Item",
        placeholder="Type item name..."
    )
    status_filter = st.selectbox(
        "📌 Stock Status",
        [
            "All",
            "Good",
            "Low",
            "Critical"
        ]
    )
    sort_by = st.selectbox(
        "↕️ Sort By",
        [
            "Default",
            "Name (A-Z)",
            "Quantity (High → Low)",
            "Quantity (Low → High)",
            "Value (High → Low)",
            "Value (Low → High)"
        ]
    )
    # =========================
    # SORT
    # =========================
    
    df["item_value"] = (
        df["quantity"] *
        df["cost_price"]
    )
    
    if sort_by == "Default":

        pass
    
    elif sort_by == "Name (A-Z)":
    
        df = df.sort_values(
            "item_name"
        )
    
    elif sort_by == "Quantity (High → Low)":
    
        df = df.sort_values(
            "quantity",
            ascending=False
        )
    
    elif sort_by == "Quantity (Low → High)":
    
        df = df.sort_values(
            "quantity"
        )
    
    elif sort_by == "Value (High → Low)":
    
        df = df.sort_values(
            "item_value",
            ascending=False
        )
    
    elif sort_by == "Value (Low → High)":
    
        df = df.sort_values(
            "item_value"
        )
    # =========================
    # INVENTORY CARDS
    # =========================

    for _, row in df.iterrows():
        if search:

            if search.lower() not in str(
                row["item_name"]
            ).lower():
        
                continue
        

        qty = int(row["quantity"])
        min_qty = int(row["min_limit"])
        ideal_stock = int(row["ideal_stock"])
        cost_price = float(row["cost_price"])
        item_value = qty * cost_price
        # =========================
        # Last Inventory Movement
        # =========================
        
        item_history = df_history[
            df_history["item_name"]
            .astype(str)
            .str.strip()
            .str.lower()
            ==
            str(row["item_name"])
            .strip()
            .lower()
        ]
        
        if not item_history.empty:
        
            item_history = item_history.sort_values(
                "date",
                ascending=False
            )
        
            last_move = item_history.iloc[0]
        
            last_movement = str(
                last_move.get("movement", "")
            ).upper()
        
            last_date = str(
                last_move.get("date", "")
            )[:10]
        
            last_technician = str(
                last_move.get("technician", "")
            )
        
        else:
        
            last_movement = "-"
        
            last_date = "-"
        
            last_technician = "-"
        if qty <= min_qty:

            status = "🔴 Critical"
        
            card_color = "#ffe5e5"
        
        elif ideal_stock > 0 and qty < ideal_stock * 0.5:
        
            status = "🟡 Low"
        
            card_color = "#fff8d9"
        
        else:
        
            status = "🟢 Good"
        
            card_color = "#e8ffe8"
        # =========================
        # STATUS FILTER
        # =========================
        
        if status_filter != "All":
        
            if status_filter not in status:
        
                continue
        # =========================
        # Badge Color
        # =========================
        
        if "Good" in status:
            badge_color = "#28A745"
        
        elif "Low" in status:
            badge_color = "#FFC107"
        
        else:
            badge_color = "#DC3545"

        with st.container(border=True):
            # =========================
            # Card Header
            # =========================
            
            header_left, header_right = st.columns([4, 1])
            
            with header_left:
            
                st.subheader(f"📦 {row['item_name']}")
            
            with header_right:
            
                if "Critical" in status:
                    st.error("🔴 Critical")
            
                elif "Low" in status:
                    st.warning("🟡 Low")
            
                else:
                    st.success("🟢 Good")
            
            
                        
            
            c1, c2, c3, c4 = st.columns(
                [2, 2, 2, 2]
            )

            with c1:

                st.metric(
                    "📦 Quantity",
                    qty
                )

            with c2:

                st.metric(
                    "⚠️Minimum",
                    min_qty
                )

            with c3:

                st.metric(
                    "💰 Unit Cost",
                    f"{cost_price:,.0f} EGP"
                )

            with c4:

                st.metric(
                    "💵 Item Value",
                    f"{item_value:,.0f} EGP"
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
                f"Current Stock : {qty} من {ideal_stock}"
            )
            footer_left, footer_buttons = st.columns([3,3])

            with footer_left:
            
                movement_icon = "➕" if last_movement == "IN" else "➖"
            
                st.caption(
                    f"{movement_icon} {last_movement}          📅 {last_date}          👨 {last_technician}"
                )
            
            with footer_buttons:

                b1, b2, b3 = st.columns(3)
            
                with b1:
            
                    show = st.button(
                        "📜 History",
                        key=f"history_{row['item_name']}",
                        use_container_width=True
                    )
            
                with b2:

                    with st.popover(
                        "➕ Add",
                        use_container_width=True
                    ):
                
                        add_qty = st.number_input(
                            "Quantity",
                            min_value=1,
                            step=1,
                            key=f"add_qty_{row['item_name']}"
                        )
                
                        add_technician = st.text_input(
                            "Technician",
                            key=f"add_tech_{row['item_name']}"
                        )
                
                        movement_reason = st.selectbox(
                            "Movement Reason",
                            [
                                "Purchase",
                                "Supplier Delivery",
                                "Customer Return",
                                "Inventory Adjustment",
                                "Transfer From Warehouse",
                                "Other"
                                ],
                                key=f"reason_{row['item_name']}"
                            )
                        invoice_no = st.text_input(
                            "Invoice / Reference No.",
                            key=f"invoice_{row['item_name']}"
                        )
                
                        add_notes = st.text_area(
                            "Notes",
                            key=f"add_notes_{row['item_name']}"
                        )
                
                        confirm_add = st.button(
                            "✅ Confirm",
                            key=f"confirm_add_{row['item_name']}",
                            use_container_width=True
                        )
                        if confirm_add:

                            new_quantity = qty + add_qty
                        
                            df.loc[
                                df["item_name"] == row["item_name"],
                                "quantity"
                            ] = new_quantity
                        
                            st.success(
                                f"{row['item_name']} updated to {new_quantity}"
                            )
            
                with b3:
            
                    remove_stock = st.button(
                        "➖ Remove",
                        key=f"remove_{row['item_name']}",
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
