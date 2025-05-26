import streamlit as st
from form import cafe_form
from table_control import cafes_table

st.set_page_config(layout='wide')
st.title("Cafes and Coffee Shops")

with st.expander("Add New Cafe or Coffee Shop"):
    cafe_form()
cafes_table()