import streamlit as st
import pandas as pd
import requests
from datetime import datetime

# =========================
# 🔥 CONFIG
# =========================

st.set_page_config(page_title="Healthy Water Pro", layout="wide")

WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwPIG6-S1aOxIL5KvN-XF_zwW0Xu6U9ARLau_R21s_Z9MJafWuPZW8fF8NOCpxEGs0OYA/exec"

LOGO_PATH = "assets/images/logo.png"

ADMIN_PASSWORD = "HgM18082019$&)"

COMPANY_PHONE = "01286609535"


# =========================
# 🔥 SHEETS GIDs
# =========================

SHEETS = {
    "Customers": "0",
    "Maintenance": "2120582392",
    "Inventory": "1767710106",
    "Expenses": "288947510",
    "Store_Products": "1129472026",
}


# =========================
# 🔥 HELPERS
# =========================

def to_num(v):
    try:
        return float(str(v).replace(",", "")) if v not in [None, ""] else 0
    except:
        return 0


def load_data(gid):
    url = f"https://docs.google.com/spreadsheets/d/1RGDGJaP_lo2Fp2beLqAQvLulqMk2WDJKqLv2g34-ycc/export?format=csv&gid={gid}"
    try:
        df = pd.read_csv(url)
        df.columns = [str(c).strip() for c in df.columns]
        return df.fillna("")
    except:
        return pd.DataFrame()


def execute_gsheet_action(action, sheet, data=None, row_index=None):
    payload = {
        "action": action,
        "sheet": sheet,
        "data": data,
        "row_index": row_index
    }
    try:
        r = requests.post(WEB_APP_URL, json=payload, timeout=20)
        return r.status_code == 200
    except:
        return False


# =========================
# 🔥 SESSION STATE
# =========================

if "user_type" not in st.session_state:
    st.session_state.user_type = None


# =========================
# 🔥 LOAD DATA
# =========================

df_c = load_data(SHEETS["Customers"])
df_m = load_data(SHEETS["Maintenance"])
df_inv = load_data(SHEETS["Inventory"])
df_exp = load_data(SHEETS["Expenses"])
df_store = load_data(SHEETS["Store_Products"])


# =========================
# 🔐 LOGIN PAGE
# =========================

if st.session_state.user_type is None:

    st.title("🚰 Healthy Water System")

    tab1, tab2 = st.tabs(["🔒 Admin", "👤 Customer"])

    with tab1:
        pwd = st.text_input("Password", type="password")
        if st.button("Login Admin"):
            if pwd == ADMIN_PASSWORD:
                st.session_state.user_type = "admin"
                st.rerun()
            else:
                st.error("Wrong password")

    with tab2:
        phone = st.text_input("Phone Number")
        if st.button("Login Customer"):
            if phone.strip() != "":
                st.session_state.user_type = "customer"
                st.session_state.phone = phone
                st.rerun()


# =========================
# 👑 ADMIN PANEL
# =========================

elif st.session_state.user_type == "admin":

    st.sidebar.image(LOGO_PATH, use_container_width=True)

    page = st.sidebar.selectbox(
        "📌 Menu",
        [
            "Dashboard",
            "Customers",
            "Maintenance",
            "Inventory",
            "Expenses",
            "Store"
        ]
    )

    # -------------------------
    # DASHBOARD
    # -------------------------
    if page == "Dashboard":
        st.title("📊 Dashboard")

    # -------------------------
    # CUSTOMERS
    # -------------------------
   elif page == "Customers":
    st.title("👥 إدارة العملاء")

    # =========================
    # 🔍 SEARCH BAR
    # =========================
    search = st.text_input("🔍 بحث (اسم / هاتف / منطقة / ID)")

    df_show = df_c.copy()

    if search:
        df_show = df_show[
            df_show.astype(str).apply(
                lambda x: x.str.contains(search, case=False, na=False)
            ).any(axis=1)
        ]

    # =========================
    # 📍 GROUP BY AREA
    # =========================
    if "area" in df_show.columns:
        areas = df_show["area"].fillna("غير محدد").unique()
    else:
        areas = ["الكل"]

    for area in areas:
        st.markdown(f"## 📍 {area}")

        group = df_show if area == "الكل" else df_show[df_show["area"] == area]

        # =========================
        # 👤 CUSTOMER CARD
        # =========================
        for _, r in group.iterrows():

            with st.expander(f"👤 {r.get('name','')} | 📞 {r.get('phone','')}"):

                col1, col2 = st.columns(2)

                # -------------------------
                # INFO SECTION
                # -------------------------
                with col1:
                    st.write(f"📞 Phone: {r.get('phone','')}")
                    st.write(f"📞 Phone 2: {r.get('phone_1','')}")
                    st.write(f"📞 Phone 3: {r.get('phone_2','')}")
                    st.write(f"🏠 Address: {r.get('adress','')}")
                    st.write(f"📍 Area: {r.get('area','')}")
                    st.write(f"📌 Location: {r.get('location_url','')}")
                    st.write(f"🔁 Cycle: {r.get('cycle','')} شهر")

                # -------------------------
                # CONTACT BUTTONS
                # -------------------------
                phones = [
                    r.get("phone"),
                    r.get("phone_1"),
                    r.get("phone_2"),
                    r.get("phone_3"),
                    r.get("phone_4"),
                ]

                st.markdown("### 📞 تواصل سريع")

                for p in phones:
                    if str(p).strip() not in ["", "None"]:
                        st.markdown(
                            f"📱 {p} | [اتصال](tel:{p}) | [واتساب](https://wa.me/2{p})"
                        )

                # -------------------------
                # LAST VISIT + NEXT VISIT
                # -------------------------
                cust_name = r.get("name")

                cust_hist = df_m[df_m["name"] == cust_name]

                if not cust_hist.empty:
                    cust_hist = cust_hist.sort_values("visit_date", ascending=False)

                    last_visit = cust_hist.iloc[0]["visit_date"]

                    try:
                        last_date = pd.to_datetime(last_visit)
                        cycle = int(to_num(r.get("cycle", 0)))
                        next_visit = last_date + pd.Timedelta(days=cycle * 30)

                        st.info(f"📅 الزيارة القادمة: {next_visit.date()}")
                    except:
                        pass

                # -------------------------
                # MAINTENANCE HISTORY
                # -------------------------
                st.markdown("### 🛠️ سجل الصيانات")

                if not cust_hist.empty:
                    show_cols = [
                        "visit_date",
                        "P1","P2","P3",
                        "membrane",
                        "post_carbon",
                        "Calcite",
                        "infrared",
                        "other",
                        "amount",
                        "notes"
                    ]

                    st.dataframe(
                        cust_hist[show_cols],
                        use_container_width=True
                    )
                else:
                    st.warning("لا يوجد سجل صيانات")

                # -------------------------
                # DELETE BUTTON (SAFE)
                # -------------------------
                st.markdown("### ⚙️ إدارة العميل")

                if st.button(f"🗑️ حذف العميل {cust_name}", key=f"del_{cust_name}"):

                    confirm = st.checkbox("تأكيد الحذف")

                    if confirm:
                        idx = r.get("row_index", None)

                        if idx:
                            execute_gsheet_action(
                                "delete",
                                "Customers",
                                row_index=idx
                            )
                            st.success("تم الحذف")
                            st.rerun()

    # -------------------------
    # MAINTENANCE
    # -------------------------
    elif page == "Maintenance":
        st.title("🔧 Maintenance")

        st.dataframe(df_m, use_container_width=True)

    # -------------------------
    # INVENTORY
    # -------------------------
    elif page == "Inventory":
        st.title("📦 Inventory")

        st.dataframe(df_inv, use_container_width=True)

    # -------------------------
    # EXPENSES
    # -------------------------
    elif page == "Expenses":
        st.title("💵 Expenses")

        st.dataframe(df_exp, use_container_width=True)

    # -------------------------
    # STORE
    # -------------------------
    elif page == "Store":
        st.title("🛒 Store Products")

        st.dataframe(df_store, use_container_width=True)


# =========================
# 👤 CUSTOMER PANEL
# =========================

elif st.session_state.user_type == "customer":

    st.sidebar.image(LOGO_PATH, use_container_width=True)

    st.title("👤 Customer Area")

    phone = st.session_state.get("phone")

    if phone:
        user_data = df_c[df_c["phone"].astype(str) == str(phone)]

        st.subheader("📄 Your Data")
        st.dataframe(user_data)

        st.subheader("🔧 Your Maintenance History")

        cust_names = user_data["name"].tolist() if "name" in user_data.columns else []
        df_hist = df_m[df_m["name"].isin(cust_names)]

        st.dataframe(df_hist)

        st.markdown("### 📞 Contact Us")
        st.markdown(f"""
        ☎️ {COMPANY_PHONE}  
        [Call](tel:{COMPANY_PHONE}) | 
        [WhatsApp](https://wa.me/2{COMPANY_PHONE})
        """)
