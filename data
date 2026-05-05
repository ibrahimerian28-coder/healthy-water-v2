import pandas as pd

BASE_SHEET = "https://docs.google.com/spreadsheets/d/1RGDGJaP_lo2Fp2beLqAQvLulqMk2WDJKqLv2g34-ycc/export?format=csv&gid="

def load_data(gid):
    try:
        url = BASE_SHEET + str(gid)
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df.fillna("")
    except:
        return pd.DataFrame()
