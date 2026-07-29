import streamlit as st

def customer_actions(row, customer_uuid):

    col1, col2 = st.columns(2)

    edit_clicked = False
    delete_clicked = False

    with col1:

        delete_clicked = st.button(
            "🗑️ Delete",
            key=f"del_{customer_uuid}"
        )

    with col2:

        edit_clicked = st.button(
            "✏️ Edit",
            key=f"edit_{customer_uuid}"
        )

    return edit_clicked, delete_clicked
