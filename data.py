import pandas as pd
import requests
from functools import lru_cache

BASE_URL = "https://docs.google.com/spreadsheets/d/1RGDGJaP_lo2Fp2beLqAQvLulqMk2WDJKqLv2g34-ycc/export?format=csv&gid="


@lru_cache(maxsize=32)
def load_data(gid: str) -> pd.DataFrame:
    """
    تحميل بيانات من Google Sheets باستخدام GID
    مع كاش لتقليل عدد الطلبات وتحسين الأداء
    """
    try:
        url = f"{BASE_URL}{gid}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        df = pd.read_csv(pd.compat.StringIO(response.text))

        # تنظيف أسماء الأعمدة
        df.columns = [str(c).strip() for c in df.columns]

        # استبدال القيم الفارغة
        return df.fillna("")

    except requests.exceptions.RequestException as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

    except Exception as e:
        print(f"Unexpected error: {e}")
        return pd.DataFrame()