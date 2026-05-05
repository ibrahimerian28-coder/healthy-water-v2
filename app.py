import streamlit as st
import pandas as pd
import requests
from datetime import datetime, timedelta

# =========================
# CONFIG
# =========================

st.set_page_config(page_title="Healthy Water Pro", layout="wide")

WEB_APP_URL = "https://script.google.com/macros/s/AKfycbwPIG6-S1aOxIL5KvN-XF_zwW0Xu6U9ARLau_R21s_Z9MJafWuPZW8fF8NOCpxEGs0OYA/exec"

LOGO_PATH = "assets/images/logo.png"

ADMIN_PASSWORD = "HgM18082019$&)"

COMPANY_PHONE = "01286609535"


# =========================
# SHEETS
# =========================

SHEETS = {
    "Customers": "0",
    "Maintenance": "2120582392",
    "Inventory": "1767710106",
    "Expenses": "288947510",
    "Store_Products": "1129472026",
}


# =========================
# HELPERS
# =========================

def to_num(x):
    try:
        return float(str(x).replace(",", "")) if x not in ["", None] else 0
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


def call_api(action, sheet, data=None, row_index=None):
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
# SESSION
# =========================

if "user_type" not in st.session_state:
    st.session_state.user_type = None


# =========================
# LOAD DATA
# =========================

df_c = load_data(SHEETS["Customers"])
df_m = load_data(SHEETS["Maintenance"])
df_inv = load_data(SHEETS["Inventory"])
df_exp = load_data(SHEETS["Expenses"])
df_store = load_data(SHEETS["Store_Products"])


# =========================
# LOGIN
# =========================

if st.session_state.user_type is None:

    st.title("🚰 Healthy Water System")

    tab1, tab2 = st.tabs(["Admin", "Customer"])

    with tab1:
        pwd = st.text_input("Password", type="password")
        if st.button("Login Admin"):
            if pwd == ADMIN_PASSWORD:
                st.session_state.user_type = "admin"
                st.rerun()
            else:
                st.error("Wrong password")

    with tab2:
        phone = st.text_input("Phone")
        if st.button("Enter Customer"):
            if phone:
                st.session_state.user_type = "customer"
                st.session_state.phone = phone
                st.rerun()


# =========================
# ADMIN PANEL
# =========================

elif st.session_state.user_type == "admin":

    st.sidebar.image(LOGO_PATH, use_container_width=True)

    page = st.sidebar.selectbox(
        "Menu",
        ["Dashboard", "Customers", "Maintenance", "Inventory", "Expenses", "Store"]
    )

    # -------------------------
    # DASHBOARD
    # -------------------------
    if page == "Dashboard":
        st.title("📊 Dashboard")

    # -------------------------
    elif page == "Customers":
    st.title("👥 Customer Profiles")

    search = st.text_input("🔍 Search by name / phone / area")

    filtered = df_c.copy()

    if search:
        filtered = df_c[
            df_c.astype(str).apply(
                lambda x: x.str.contains(search, case=False, na=False)
            ).any(axis=1)
        ]

    for _, row in filtered.iterrows():

        with st.expander(f"👤 {row.get('name','')} | 📍 {row.get('area','')}"):

            # =========================
            # BASIC INFO
            # =========================
            st.subheader("📄 Customer Info")

            st.write(f"🏠 Address: {row.get('adress','')}")
            st.write(f"📍 Area: {row.get('area','')}")
            st.write(f"📅 Install Date: {row.get('install_date','')}")
            st.write(f"🔁 Cycle: {row.get('cycle','')} months")

            # =========================
            # PHONES
            # =========================
            st.subheader("📞 Phones")

            phones = [
                row.get("phone"),
                row.get("phone_1"),
                row.get("phone_2"),
                row.get("phone_3"),
                row.get("phone_4"),
            ]

            for ph in phones:
                if str(ph).strip():
                    c1, c2 = st.columns([1,2])
                    c1.write(f"📱 {ph}")
                    c2.markdown(
                        f"[📞 Call](tel:{ph}) | [💬 WhatsApp](https://wa.me/2{ph})"
                    )

            # =========================
            # MAINTENANCE HISTORY
            # =========================
            st.subheader("🔧 Maintenance History")

            cust_hist = df_m[df_m["name"] == row["name"]].copy()

            if not cust_hist.empty:

                cust_hist = cust_hist.sort_values("visit_date", ascending=False)

                # عرض الأعمدة المطلوبة
                show_cols = [
                    "visit_date",
                    "P1","P2","P3",
                    "membrane","post_carbon","Calcite","infrared",
                    "other","amount","notes"
                ]

                for col in show_cols:
                    if col not in cust_hist.columns:
                        cust_hist[col] = ""

                # تحويل true/false
                check_cols = ["P1","P2","P3","membrane","post_carbon","Calcite","infrared"]

                for col in check_cols:
                    cust_hist[col] = cust_hist[col].apply(
                        lambda x: "✅" if str(x).lower() in ["true","1","yes","y","✔","✅"] else "❌"
                    )

                st.dataframe(
                    cust_hist[show_cols],
                    use_container_width=True,
                    hide_index=True
                )

                # =========================
                # NEXT VISIT CALCULATION
                # =========================
                try:
                    last_date = pd.to_datetime(cust_hist.iloc[0]["visit_date"])
                    cycle = int(row.get("cycle", 0))
                    next_visit = last_date + timedelta(days=cycle * 30)

                    st.info(f"📅 Next Visit: {next_visit.date()}")
                except:
                    st.warning("⚠️ Cannot calculate next visit")

            else:
                st.warning("No maintenance history found")

            # =========================
            # ACTION BUTTONS
            # =========================
            st.subheader("⚙️ Actions")

            col1, col2, col3 = st.columns(3)

            # ADD MAINTENANCE
            if col1.button("➕ Add Maintenance", key=f"add_m_{row.name}"):
                st.session_state.selected_customer = row["name"]
                st.session_state.page_redirect = "Maintenance"
                st.rerun()

            # DELETE CUSTOMER
            if col2.button("🗑️ Delete", key=f"del_{row.name}"):

                confirm = st.warning("Are you sure you want to delete this customer?")
                if st.button("Yes Delete", key=f"confirm_del_{row.name}"):
                    call_api("delete", "Customers", row_index=row.get("row_index"))
                    st.success("Deleted successfully")
                    st.rerun()

            # SHARE
            if col3.button("📤 Share", key=f"share_{row.name}"):
                share_text = f"""
Customer: {row['name']}
Phone: {row.get('phone','')}
Area: {row.get('area','')}
                """
                st.code(share_text)


    # -------------------------
    # MAINTENANCE
    # -------------------------
    elif page == "Maintenance":
        st.title("🔧 Maintenance")
        st.dataframe(df_m)

    # -------------------------
    # INVENTORY
    # -------------------------
    elif page == "Inventory":
        st.title("📦 Inventory")
        st.dataframe(df_inv)

    # -------------------------
    # EXPENSES
    # -------------------------
    elif page == "Expenses":
        st.title("💵 Expenses")
        st.dataframe(df_exp)

    # -------------------------
    # STORE
    # -------------------------
    elif page == "Store":
        st.title("🛒 Store")
        st.dataframe(df_store)


# =========================
# CUSTOMER PANEL
# =========================

elif st.session_state.user_type == "customer":

    st.sidebar.image(LOGO_PATH, use_container_width=True)

    st.title("👤 My Account")

    phone = st.session_state.get("phone")

    if phone:

        user = df_c[df_c["phone"].astype(str) == str(phone)]

        st.subheader("📄 My Data")
        st.dataframe(user)

        names = user["name"].tolist() if "name" in user.columns else []

        history = df_m[df_m["name"].isin(names)]

        st.subheader("🔧 Maintenance History")
        st.dataframe(history)

        st.markdown("### 📞 Contact Company")
        st.markdown(f"""
        ☎️ {COMPANY_PHONE}  
        [Call](tel:{COMPANY_PHONE}) | 
        [WhatsApp](https://wa.me/2{COMPANY_PHONE})
        """)
