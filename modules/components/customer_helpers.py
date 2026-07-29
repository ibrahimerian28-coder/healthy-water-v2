# =========================
# HELPERS
# =========================

def clean_phone(p):

    if pd.isna(p):
        return ""

    p = str(p).strip()

    if p.lower() in ["nan", "none"]:
        return ""

    return p

def wa_link(phone):

    phone = clean_phone(phone)

    phone = phone.replace(" ", "")

    if phone.startswith("0"):
        phone = "2" + phone

    return f"https://wa.me/{phone}"
