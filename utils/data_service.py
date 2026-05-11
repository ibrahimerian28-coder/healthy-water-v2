import pandas as pd

BASE_URL = "https://docs.google.com/spreadsheets/d/1RGDGJaP_lo2Fp2beLqAQvLulqMk2WDJKqLv2g34-ycc/export?format=csv"

def load_sheet(gid: str):

    url = f"{BASE_URL}&gid={gid}"

    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df.fillna("")
    except Exception as e:
        print("Load error:", e)
        return pd.DataFrame()
