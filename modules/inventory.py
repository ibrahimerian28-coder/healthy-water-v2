import streamlit as st
from utils.data_service import load_sheet
from datetime import datetime

def app():

    st.title("📦 Inventory")

    gid = st.session_state.SHEETS["Inventory"]
    df = load_sheet(gid)

    history_gid = st.session_state.SHEETS["Inventory_History"]
df_history = load_sheet(history_gid)

if "date" in df_history.columns:
    df_history["date"] = df_history["date"].astype(str)

st.write("عدد الأصناف:", len(df))

for _, row in df.iterrows():

    with st.container(border=True):

        col1, col2, col3 = st.columns([4,2,2])

        with col1:
            st.markdown(f"### 📦 {row['item_name']}")

        with col2:
            st.metric(
                "الكمية",
                row["quantity"]
            )

        with col3:

            show = st.button(
                "📜 History",
                key=f"history_{row['item_name']}"
            )

        if show:

            history = df_history[
                df_history["item_name"]
                .astype(str)
                .str.strip()
                .str.lower()
                ==
                str(row["item_name"])
                .strip()
                .lower()
            ]

            if history.empty:

                st.info("لا توجد حركات لهذا الصنف")

            else:

                history = history.sort_values(
                    "date",
                    ascending=False
                )

                st.dataframe(
                    history,
                    hide_index=True,
                    use_container_width=True
                )
