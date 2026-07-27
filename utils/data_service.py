import pandas as pd
import requests
print("######## USING utils/data_service.py ########")

# =========================
# CONFIG
# =========================

SHEET_ID = "1RGDGJaP_lo2Fp2beLqAQvLulqMk2WDJKqLv2g34-ycc"

APP_SCRIPT_URL = "https://script.google.com/macros/s/AKfycby2ZijzCzTSjUKJ9CtoMXxBv3vX3sq5J0rod3y12XVlHl2vGx_RVAdJaSYIK_1qPnr-wg/exec"

BASE_URL = f"https://docs.google.com/spreadsheets/d/{SHEET_ID}/export?format=csv"



# =========================
# 📌 LOAD SHEET (READ ONLY)
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
# 📌 API CALL (GOOGLE APPS SCRIPT)
# =========================

def call_api(action, sheet, data=None, row_index=None, uuid=None):

    payload = {
        "action": action,
        "sheet": sheet,
        "data": data,
        "row_index": row_index,
        "uuid": uuid
    }

    try:
        r = requests.post(
            APP_SCRIPT_URL,
            json=payload,
            timeout=20
        )

        response = r.text.strip()

        print("REQUEST URL:", APP_SCRIPT_URL)
        print("Status Code:", r.status_code)
        print("RAW RESPONSE:", response)

        import streamlit as st

        st.write("REQUEST URL:", APP_SCRIPT_URL)
        st.write("Status Code:", r.status_code)
        st.write("RAW RESPONSE:", response)

        return response.startswith("OK")

    except Exception as e:
        print("API ERROR:", e)
        st.error(e)
        return False


# =========================
# 📌 CREATE (APPEND)
# =========================

def add_row(sheet, data):
    return call_api(
        action="append",
        sheet=sheet,
        data=data
    )


# =========================
# 📌 UPDATE BY UUID (NEW SYSTEM)
# =========================

def update_row(sheet, uuid_value, data):

    return call_api(
        action="update",
        sheet=sheet,
        data=data,
        uuid=uuid_value
    )


# =========================
# 📌 DELETE BY UUID (NEW SYSTEM)
# =========================

def delete_row_by_uuid(sheet, uuid_value):
    return call_api(
        action="delete",
        sheet=sheet,
        uuid=uuid_value
    )
