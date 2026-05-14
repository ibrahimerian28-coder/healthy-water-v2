import pandas as pd
from data import load_data

# غير الرقم ده حسب الشيت بتاعك (GID الخاص بالعملاء)
CUSTOMERS_GID = "0"


# =========================
# 📌 1. جلب كل العملاء
# =========================
def get_customers():
    df = load_data(CUSTOMERS_GID)
    return df


# =========================
# 📌 2. جلب عميل بالـ UUID
# =========================
def get_customer_by_id(customer_id: str):
    df = load_data(CUSTOMERS_GID)

    if "uuid" not in df.columns:
        return None

    result = df[df["uuid"] == customer_id]

    if result.empty:
        return None

    return result.to_dict(orient="records")[0]


# =========================
# 📌 3. إضافة عميل (مبدئيًا)
# =========================
def add_customer(data: dict):
    """
    data مثال:
    {
        "uuid": "123",
        "name": "Ahmed",
        "phone": "010..."
    }
    """
    print("➕ Add customer:", data)
    return True


# =========================
# 📌 4. تعديل عميل (مبدئيًا)
# =========================
def update_customer(customer_id: str, updated_data: dict):
    print(f"✏️ Update customer {customer_id}:", updated_data)
    return True


# =========================
# 📌 5. حذف عميل (مبدئيًا)
# =========================
def delete_customer(customer_id: str):
    print(f"🗑️ Delete customer {customer_id}")
    return True
def delete_row_by_uuid(sheet_name, uuid_value):
    df = load_sheet(sheet_name)

    df = df[df["uuid"] != uuid_value]

    # إعادة رفع الداتا بعد الحذف
    return save_sheet(sheet_name, df)
