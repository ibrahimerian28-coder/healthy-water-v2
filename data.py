import pandas as pd

BASE_URL = "https://docs.google.com/spreadsheets/d/1RGDGJaP_lo2Fp2beLqAQvLulqMk2WDJKqLv2g34-ycc/export?format=csv&gid="

def load_data(gid):
    try:
        df = pd.read_csv(BASE_URL + gid)
        df.columns = [str(c).strip() for c in df.columns]
        return df.fillna("")
    except:
        return pd.DataFrame()
