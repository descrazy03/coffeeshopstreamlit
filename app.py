import streamlit as st
from form import cafe_form
from table_control import cafes_table
import streamlit as st
from database.models import Base, CafeBase
from database.setup import engine
import yaml
from yaml.loader import SafeLoader
from controller import Controller
import pandas as pd
import numpy as np
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
    
    # create back up of database
    with st.popover("Dez' Special Button"):
        cafes_controller = Controller('cafes')
        all_cafes = cafes_controller.get_all()
        cafes_df = all_cafes.to_csv().encode('utf-8')
        st.subheader("Get All Data")
        download_btn = st.download_button("Download", data=cafes_df, mime="text/csv")
        st.subheader("Append Data")
        upload_btn = st.file_uploader("Upload File", type="csv")
        commit_change_btn = st.button("Commit Changes")
        # handle appending and updating database entries
        if upload_btn != None and commit_change_btn:
            existing_ids = all_cafes['id'].values.tolist()
            uploaded_file = pd.read_csv(upload_btn)
            df_cols = all_cafes.columns
            for col,row in uploaded_file.iterrows():
                curr_row = CafeBase(id=row.id,
                                    name=row['name'] if type(row['name']) != float else "",
                                    address=row.address if type(row.address) != float else "",
                                    has_restroom=row.has_restroom,
                                    restroom_pass=row.restroom_pass if type(row.restroom_pass) != float else "",
                                    has_wifi = row.has_wifi,
                                    wifi_pass=row.wifi_pass if type(row.wifi_pass) != float else "",
                                    has_outlets=row.has_outlets,
                                    notes=row.notes if type(row.notes) != float else "",
                                    is_fav=row.is_fav,
                                    mon_open=row.mon_open if type(row.mon_open) != float else "",
                                    mon_close=row.mon_close if type(row.mon_close) != float else "",
                                    tue_open=row.tue_open if type(row.tue_open) != float else "",
                                    tue_close=row.tue_close if type(row.tue_close) != float else "",
                                    wed_open=row.wed_open if type(row.wed_open) != float else "",
                                    wed_close=row.wed_close if type(row.wed_close) != float else "",
                                    thu_open=row.thu_open if type(row.thu_open) != float else "",
                                    thu_close=row.thu_close if type(row.thu_close) != float else "",
                                    fri_open=row.fri_open if type(row.fri_open) != float else "",
                                    fri_close=row.fri_close if type(row.fri_close) != float else "",
                                    sat_open=row.sat_open if type(row.sat_open) != float else "",
                                    sat_close=row.sat_close if type(row.sat_close) != float else "",
                                    sun_open=row.sun_open if type(row.sun_open) != float else "",
                                    sun_close=row.sun_close if type(row.sun_close) != float else "",
                                    updated_at=row.updated_at)
                if curr_row.id in existing_ids:
                    # determine if existing row should be updated
                    og_row = cafes_controller.get_one(curr_row.id).iloc[0]
                    og_row=og_row.replace(0, False).replace(1, True).to_dict()
                    if curr_row.model_dump() != og_row:
                        curr_row.name = curr_row.name.replace("'", "''")
                        curr_row.address = curr_row.address.replace("'", "''")
                        curr_row.restroom_pass = curr_row.restroom_pass.replace("'", "''")
                        curr_row.wifi_pass = curr_row.wifi_pass.replace("'", "''")
                        curr_row.notes = curr_row.notes.replace("'", "''")
                        cafes_controller.update(updates=curr_row, id=curr_row.id)
                else:
                    curr_row.id = None
                    cafes_controller.post(curr_row)
            st.rerun()
        
            
elif st.session_state['authentication_status'] is False:
    st.error('Incorrect Username/Password')
elif st.session_state['authentication_status'] is None:
    st.warning('Please enter username and password')