import streamlit as st
from utils.data_service import (
    load_sheet,
    update_row
)

import pandas as pd


def check_inventory(parts_used, inventory_gid):

    df = load_sheet(inventory_gid)

    df.columns = df.columns.str.strip()

    errors = []

    for part in parts_used:

        item = part["item"].strip().lower()
        qty_needed = int(part["qty"])

        match = df[
            df["item_name"]
            .astype(str)
            .str.strip()
            .str.lower()
            == item
        ]

        if match.empty:

            errors.append(
                f"{part['item']} غير موجود بالمخزون."
            )

            continue

        available = int(
            pd.to_numeric(
                match.iloc[0]["quantity"],
                errors="coerce"
            ) or 0
        )

        if available < qty_needed:

            errors.append(
                f"{part['item']} : المتوفر {available} - المطلوب {qty_needed}"
            )

    st.write("===== INVENTORY =====")
    st.write(df)

    st.write("===== USED PARTS =====")
    st.write(parts_used)

    st.write("===== ERRORS =====")
    st.write(errors)

    return errors


def deduct_inventory(parts_used, inventory_gid):

    df = load_sheet(inventory_gid)

    df.columns = df.columns.str.strip()

    for part in parts_used:

        st.write("خصم:", part["item"], part["qty"])

        item = part["item"].strip().lower()
        qty_used = int(part["qty"])

        match = df[
            df["item_name"]
            .astype(str)
            .str.strip()
            .str.lower()
            == item
        ]

        st.write(match)

        if match.empty:
            continue

        row = match.iloc[0]

        current_qty = int(
            pd.to_numeric(
                row["quantity"],
                errors="coerce"
            ) or 0
        )

        new_qty = current_qty - qty_used

       update_row(
           "Inventory",
           "",
           {
               "item_name": row["item_name"],
               "quantity": new_qty
           }
       )
