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
            match.iloc[0]["quantity"]
        )

        if available < qty_needed:

            errors.append(
                f"{part['item']} : المتوفر {available} - المطلوب {qty_needed}"
            )

    return errors
