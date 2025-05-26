import streamlit as st
from form import cafe_form
from table_control import cafes_table
import streamlit as st
from database.models import Base
from database.setup import engine
import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth


st.set_page_config(layout='wide')
st.title("Cafes and Coffee Shops")
Base.metadata.create_all(bind=engine)

with open('./config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

auth = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

try:
    auth.login(location='sidebar', clear_on_submit=True)
    with open('./config.yaml', 'w') as file:
        yaml.dump(config, file, default_flow_style=False)

except Exception as e:
    st.error(e)
if st.session_state['authentication_status']:
    auth.logout()
    with st.expander("Add New Cafe or Coffee Shop"):
        cafe_form()
    cafes_table()
elif st.session_state['authentication_status'] is False:
    st.error('Incorrect Username/Password')
elif st.session_state['authentication_status'] is None:
    st.warning('Please enter username and password')