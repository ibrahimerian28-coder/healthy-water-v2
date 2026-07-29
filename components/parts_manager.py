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

    return used_parts
