import pandas as pd
import requests

# =========================
# CONFIG
# =========================

SHEET_ID = "1RGDGJaP_lo2Fp2beLqAQvLulqMk2WDJKqLv2g34-ycc"

APP_SCRIPT_URL = "https://script.google.com/macros/s/AKfycbzH9NgXhbWMTKJv8SKd6t8T75VXVssJlABeMxo_BOGss9vVxighDwW-MuPsxUKcXoxDsA/exec"

BASE_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"

# =========================
# LOAD DATA
# =========================

def load_sheet(gid):

    url = f"{BASE_URL}&gid={gid}"

    try:
        df = pd.read_csv(url)

        df.columns = df.columns.str.strip()

        return df.fillna("")

    except Exception as e:

        print("LOAD ERROR:", e)

        return pd.DataFrame()

# =========================
# API CALL
# =========================

def call_api(action, sheet, data=None, row_index=None):

    payload = {
        "action": action,
        "sheet": sheet,
        "data": data,
        "row_index": row_index
    }

    try:

        r = requests.post(
            APP_SCRIPT_URL,
            json=payload,
            timeout=20
        )

        response = r.text.strip()

        print("API RESPONSE:", response)

        return response.startswith("OK")

    except Exception as e:

        print("API ERROR:", e)

        return False

# =========================
# ADD ROW
# =========================

def add_row(sheet, data):

    return call_api(
        action="append",
        sheet=sheet,
        data=data
    )

# =========================
# UPDATE ROW
# =========================

def update_row(sheet, row_index, data):

    return call_api(
        action="update",
        sheet=sheet,
        data=data,
        row_index=row_index
    )

# =========================
# DELETE ROW
# =========================

def delete_row(sheet, row_index):

    return call_api(
        action="delete",
        sheet=sheet,
        row_index=row_index
    )
