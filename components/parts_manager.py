import streamlit as st
import pandas as pd


def render_parts_manager(df_inventory):

    st.subheader("🧩 Parts Used")

    standard_parts = [
        "P1",
        "P2",
        "P3",
        "Membrane",
        "Post Carbon",
        "Calcite",
        "Infrared"
    ]

    used_parts = []

    st.markdown("### Standard Filters")

    for part in standard_parts:

        selected = st.checkbox(
            part,
            key=f"chk_{part}"
        )
        
        if selected:
            
            qty = st.number_input(
                f"{part} Qty",
                min_value=1,
                value=1,
                step=1,
                key=f"qty_{part}"
            )

            used_parts.append({
                "item": part,
                "qty": qty
            })

    st.divider()
    # =========================
    # OTHER PARTS
    # =========================

    st.markdown("### Other Parts")
    st.success("وصلنا إلى Other Parts")

    excluded_items = {
        "p1",
        "p2",
        "p3",
        "membrane",
        "post carbon",
        "calcite",
        "infrared"
    }

    inventory_items = []

    if "item_name" in df_inventory.columns:

        inventory_items = (
            df_inventory["item_name"]
            .dropna()
            .astype(str)
            .str.strip()
            .tolist()
        )

        inventory_items = [
            item
            for item in inventory_items
            if item.lower() not in excluded_items
        ]
        st.write(inventory_items)

    if "other_parts_list" not in st.session_state:

        st.session_state.other_parts_list = []


    col1, col2 = st.columns([3,1])


    with col1:

        selected_part = st.selectbox(
            "Select Part",
            [""] + sorted(inventory_items),
            key="selected_other_part"
        )


    with col2:

        part_qty = st.number_input(
            "Qty",
            min_value=1,
            value=1,
            step=1,
            key="other_part_qty"
        )


    if st.button(
        "➕ Add Part",
        key="add_other_part"
    ):

        if selected_part:

            exists = False

            for item in st.session_state.other_parts_list:

                if item["item"] == selected_part:

                    item["qty"] += part_qty
                    exists = True


            if not exists:

                st.session_state.other_parts_list.append(
                    {
                        "item": selected_part,
                        "qty": part_qty
                    }
                )


    # عرض القطع المختارة

    if st.session_state.other_parts_list:

        st.markdown("#### Selected Parts")

        for index, item in enumerate(
            st.session_state.other_parts_list
        ):

            c1, c2, c3 = st.columns([3,1,1])

            with c1:
                st.write(item["item"])

            with c2:
                st.write(
                    f"Qty: {item['qty']}"
                )

            with c3:

                if st.button(
                    "🗑️",
                    key=f"delete_part_{index}"
                ):

                    st.session_state.other_parts_list.pop(index)
                    st.rerun()


        used_parts.extend(
            st.session_state.other_parts_list
        )

    return used_parts
