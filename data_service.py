import pandas as pd
from data import load_data, save_data

# =========================
# 📌 SHEETS CONFIG
# =========================

CUSTOMERS_GID = "0"
MAINTENANCE_GID = "1"  # غيّر الرقم حسب شيت الصيانة عندك


# =========================
# 📌 CUSTOMERS - READ
# =========================

def get_customers():
    df = load_data(CUSTOMERS_GID)
    return df


def get_customer_by_id(customer_id: str):
    df = load_data(CUSTOMERS_GID)

    if "uuid" not in df.columns:
        return None

    result = df[df["uuid"] == customer_id]

    if result.empty:
        return None

    return result.to_dict(orient="records")[0]


# =========================
# 📌 CUSTOMERS - CREATE
# =========================

def add_customer(data: dict):
    df = load_data(CUSTOMERS_GID)

    if df is None:
        df = pd.DataFrame()

    df = pd.concat([df, pd.DataFrame([data])], ignore_index=True)

    return save_data(CUSTOMERS_GID, df)


# =========================
# 📌 CUSTOMERS - UPDATE
# =========================

def update_customer(customer_id: str, updated_data: dict):
    df = load_data(CUSTOMERS_GID)

    if "uuid" not in df.columns:
        return False

    for key, value in updated_data.items():
        df.loc[df["uuid"] == customer_id, key] = value

    return save_data(CUSTOMERS_GID, df)


# =========================
# 📌 CUSTOMERS - DELETE
# =========================

def delete_customer(customer_id: str):
    df = load_data(CUSTOMERS_GID)

    if "uuid" not in df.columns:
        return False

    df = df[df["uuid"] != customer_id]

    return save_data(CUSTOMERS_GID, df)


# =========================
# 📌 MAINTENANCE - UPDATE
# =========================

def update_maintenance(uuid_value: str, updated_data: dict):
    df = load_data(MAINTENANCE_GID)

    if "uuid" not in df.columns:
        return False

    for key, value in updated_data.items():
        df.loc[df["uuid"] == uuid_value, key] = value

    return save_data(MAINTENANCE_GID, df)


# =========================
# 📌 MAINTENANCE - DELETE
# =========================

def delete_maintenance(uuid_value: str):
    df = load_data(MAINTENANCE_GID)

    if "uuid" not in df.columns:
        return False

    df = df[df["uuid"] != uuid_value]

    return save_data(MAINTENANCE_GID, df)


# =========================
# 📌 HELPERS
# =========================

def get_maintenance():
    return load_data(MAINTENANCE_GID)
