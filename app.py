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
        if st.button("Login"):
            if pwd == ADMIN_PASSWORD:
                st.session_state.user_type = "admin"
                st.rerun()
            else:
                st.error("Wrong password")

    with tab2:
        phone = st.text_input("Phone")
        if st.button("Enter"):
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
    # CUSTOMERS (FIXED + CLEAN)
    # -------------------------
    elif page == "Customers":

        st.title("👥 Customer Profiles")

        search = st.text_input("🔍 Search by name / phone / area")

        # =========================
        # FILTER
        # =========================
        filtered = df_c.copy()

        if search:
            filtered = df_c[
                df_c.astype(str).apply(
                     lambda x: x.str.contains(search, case=False, na=False)
                 ).any(axis=1)
            ]

        # تنظيف المناطق
        filtered["area"] = filtered["area"].fillna("غير محدد")

        # =========================
        # GROUP BY AREA
        # =========================
        for area in sorted(filtered["area"].unique()):

            st.markdown(f"## 📍 {area}")

            area_df = filtered[filtered["area"] == area]
    
            for _, row in area_df.iterrows():

                with st.expander(f"👤 {row.get('name','')} | 📞 {row.get('phone','')}"):

                    # =========================
                    # BASIC INFO
                    # =========================
                    st.subheader("📄 Customer Info")

                    st.write(f"🏠 Address: {row.get('adress','')}")
                    st.write(f"📍 Area: {row.get('area','')}")
                    st.write(f"📅 Install Date: {row.get('install_date','')}")
                    st.write(f"🔁 Cycle: {row.get('cycle','')} months")

                    # =========================
                    # PHONES (NO NONE FIX)
                    # =========================
                    st.subheader("📞 Phones")

                    phones = [
                        row.get("phone"),
                        row.get("phone_1"),
                        row.get("phone_2"),
                        row.get("phone_3"),
                        row.get("phone_4"),
                    ]

                    clean_phones = [
                        p for p in phones
                        if str(p).strip() and str(p).lower() != "none"
                    ]

                    for ph in clean_phones:
                        c1, c2 = st.columns([1, 2])
                        c1.write(f"📱 {ph}")
                        c2.markdown(
                            f"[📞 Call](tel:{ph}) | [💬 WhatsApp](https://wa.me/2{ph})"
                        )

                    # =========================
                    # ACTIONS
                    # =========================
                    st.subheader("⚙️ Actions")

                    col1, col2 = st.columns(2)

                    # -------------------------
                    # DELETE CUSTOMER
                    # -------------------------
                    with col1:

                        if st.button(
                            "🗑️ Delete",
                            key=f"del_{row.name}_{row.get('phone','')}"
                        ):

                            confirm = st.checkbox(
                                f"Confirm delete {row.get('name','')}",
                                key=f"confirm_{row.name}"
                            )

                            if confirm:

                                success = call_api(
                                    action="delete",
                                    sheet="Customers",
                                    row_index=int(row.get("row_index", 0))
                                )

                                if success:
                                    st.success("Customer deleted successfully")
                                    st.rerun()
                                else:
                                    st.error("Delete failed - check row_index")

                    # -------------------------
                    # EDIT CUSTOMER
                    # -------------------------
                    with col2:

                        with st.expander("✏️ Edit Customer"):

                            new_name = st.text_input(
                                "Name",
                                value=row.get("name", ""),
                                key=f"name_{row.name}"
                            )

                            new_phone = st.text_input(
                                "Phone",
                                value=row.get("phone", ""),
                                key=f"phone_{row.name}"
                            )

                            new_phone1 = st.text_input(
                                "Phone 1",
                                value=row.get("phone_1", ""),
                                key=f"phone1_{row.name}"
                            )

                            new_phone2 = st.text_input(
                                "Phone 2",
                                value=row.get("phone_2", ""),
                                key=f"phone2_{row.name}"
                            )

                            new_phone3 = st.text_input(
                                "Phone 3",
                                value=row.get("phone_3", ""),
                                key=f"phone3_{row.name}"
                            )

                            new_phone4 = st.text_input(
                                "Phone 4",
                                value=row.get("phone_4", ""),
                                key=f"phone4_{row.name}"
                            )

                            new_address = st.text_input(
                                "Address",
                                value=row.get("adress", ""),
                                key=f"addr_{row.name}"
                            )

                            new_area = st.text_input(
                                "Area",
                                value=row.get("area", ""),
                                key=f"area_{row.name}"
                            )

                            new_location = st.text_input(
                                "Location URL",
                                value=row.get("location_url", ""),
                                key=f"loc_{row.name}"
                            )

                            new_install = st.text_input(
                                "Install Date",
                                value=row.get("install_date", ""),
                                key=f"inst_{row.name}"
                            )

                            new_cycle = st.text_input(
                                "Cycle",
                                value=row.get("cycle", ""),
                                key=f"cycle_{row.name}"
                            )

                            new_status = st.text_input(
                                "Status",
                                value=row.get("status", ""),
                                key=f"status_{row.name}"
                            )

                            if st.button("💾 Save", key=f"save_{row.name}"):
    
                                updated_data = [
                                    new_name,
                                    new_phone,
                                    new_phone1,
                                    new_phone2,
                                    new_phone3,
                                    new_phone4,
                                    new_address,
                                    new_area,
                                    new_location,
                                    new_install,
                                    new_cycle,
                                    new_status,
                                ]

                                success = call_api(
                                    action="update",
                                    sheet="Customers",
                                    data=updated_data,
                                    row_index=int(row.get("row_index", 0))
                                )

                                if success:
                                    st.success("Updated successfully")
                                    st.rerun()
                                else:
                                    st.error("Update failed")

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

        st.markdown("### 📞 Contact")
        st.markdown(f"""
        ☎️ {COMPANY_PHONE}  
        [Call](tel:{COMPANY_PHONE}) | 
        [WhatsApp](https://wa.me/2{COMPANY_PHONE})
        """)
