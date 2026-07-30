from datetime import datetime
from utils.data_service import add_row


def add_inventory_history(
    item_name,
    qty,
    movement_type,
    reference,
    technician,
    history_gid
):
    """
    movement_type:
        OUT = خصم
        IN  = إضافة
        ADJUST = تعديل
    """

    row = [
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),  # الحركة
        item_name,                                     # الصنف
        qty,                                           # الكمية
        movement_type,                                 # نوع الحركة
        reference,                                     # رقم الزيارة أو السبب
        technician                                     # الفني
    ]

    return add_row(
        "Inventory_History",
        row
    )
