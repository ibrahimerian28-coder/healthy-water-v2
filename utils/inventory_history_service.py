from datetime import datetime
import uuid

from utils.data_service import add_row


def add_inventory_history(
    movement,
    item_name,
    quantity,
    reference,
    technician,
    notes=""
):
    row = [
        str(uuid.uuid4()),                              # uuid
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),   # date
        movement,                                       # movement
        item_name,                                      # item_name
        quantity,                                       # quantity
        reference,                                      # reference
        technician,                                     # technician
        notes                                           # notes
    ]

    return add_row(
        "Inventory_History",
        row
    )
