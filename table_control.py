from controller import Controller
from database.models import CafeBase
from form import cafe_form
import streamlit as st
import pandas as pd

cafes = Controller("cafes")

def cafes_table(fav_only=False):
    
    # filter form
    if fav_only == False:
        with st.popover("Filter Cafes", use_container_width=True):
            weekdays = ["Monday", 'Tuesday', 'Wednesday',
                        'Thursday', 'Friday', 'Saturday', 'Sunday']
            filters = ['Has Restrooms', "Has Wifi", "Has Outlets"]
            st.header("Apply Filters")
            st.subheader("Filter by Day and Hours", divider=True)
            day_filter = st.selectbox("Pick Day of the Week", options=weekdays, index=None)
            time_filter = st.time_input("Pick Time", value=None)
            st.subheader("Filter by Amenities", divider=True)
            filter_select = st.multiselect("Restrooms, Wifi, and Outlets", options=filters)
        
        cafes_db = cafes.get_all()
    
        # filter functionality for day of the week and time
        if (day_filter != None) and (time_filter != None):

            days_cols = [['mon_open', 'mon_close'], ['tue_open', 'tue_close'], ['wed_open', 'wed_close'],
                        ['thu_open', 'thu_close'], ['fri_open', 'fri_close'], ['sat_open', 'sat_close'],
                        ['sun_open', 'sun_close']]
            days_dict = dict(zip(weekdays, days_cols)) 
            selected_day = days_dict[day_filter]
            try:
                cafes_db[selected_day[0]] = pd.to_datetime(cafes_db[selected_day[0]], format="%H:%M").dt.time
                cafes_db[selected_day[1]] = pd.to_datetime(cafes_db[selected_day[1]], format="%H:%M").dt.time
                cafes_db = cafes_table.where((time_filter >= cafes_db[selected_day[0]]) & (time_filter <= cafes_table[selected_day[1]]))
            except:
                pass
    

        # filter functionality for amenities
        if len(filter_select) > 0:
            if "Has Wifi" in filter_select:
                cafes_db = cafes_db.where(cafes_db.has_wifi == True)
            if "Has Restrooms" in filter_select:
                cafes_db = cafes_db.where(cafes_db.has_restroom == True)
            if "Has Outlets" in filter_select:
                cafes_db = cafes_db.where(cafes_db.has_outlets == True)
    else:
        cafes_db = cafes.get_all().where(cafes.get_all()['is_fav'] == True)

    # interactive table for cafes
    cafes_df = st.dataframe(cafes_db.dropna(),
                            column_order=["name", "address", "is_fav"],
                            column_config={"name": "Name",
                                           "address": "Address",
                                           "is_fav": st.column_config.CheckboxColumn("Is Favorite")},
                            on_select='rerun',
                            selection_mode='single-row',
                            hide_index=True,
                            use_container_width=True,
                            key="interactive")
    
    # table selection funtionality
    if cafes_df.selection.rows:
        cafe_idx = cafes_df.selection.rows
        cafe_row = cafes_db.dropna().iloc[cafe_idx]
        cafe_id = cafe_row['id'].iloc[0]

        st.subheader(f"Details for {cafe_row['name'].iloc[0]}")
        restroom_col, wifi_col, outlets_col = st.columns(3)
        with restroom_col:
            st.metric("Has Restroom?", "Yes" if cafe_row['has_restroom'].iloc[0] else "No")
            if cafe_row['restroom_pass'].iloc[0] != '':
                st.metric("Restroom Password", cafe_row['restroom_pass'].iloc[0])
        with wifi_col:
            st.metric("Has Wifi?", "Yes" if cafe_row['has_wifi'].iloc[0] else "No")
            if cafe_row['wifi_pass'].iloc[0] != '':
                st.metric("Wifi Password", cafe_row['wifi_pass'].iloc[0])
        with outlets_col:
            st.metric("Has Outlets?", "Yes" if cafe_row['has_outlets'].iloc[0] else "No")

        with st.container(border=True):
            st.subheader("Additional Notes", divider=True)
            st.write(cafe_row['notes'].iloc[0])
        
        st.subheader("Hours Information")

        hours_df = pd.DataFrame({"Monday": [cafe_row['mon_open'].iloc[0], cafe_row['mon_close'].iloc[0]],
                                 "Tuesday": [cafe_row['tue_open'].iloc[0], cafe_row['tue_close'].iloc[0]],
                                 "Wednesday": [cafe_row['wed_open'].iloc[0], cafe_row['wed_close'].iloc[0]],
                                 "Thursday": [cafe_row['thu_open'].iloc[0], cafe_row['thu_close'].iloc[0]],
                                 "Friday": [cafe_row['fri_open'].iloc[0], cafe_row['fri_close'].iloc[0]],
                                 "Saturday": [cafe_row['sat_open'].iloc[0], cafe_row['sat_close'].iloc[0]],
                                 "Sunday": [cafe_row['sun_open'].iloc[0], cafe_row['sun_close'].iloc[0]]})
        hours_table = st.dataframe(hours_df,
                                   hide_index=True,
                                   use_container_width=True)
        st.write(f"Last Updated: {cafe_row['updated_at'].iloc[0]}") 
        if fav_only == False:
            with st.expander("Update Cafe"):
                cafe_form(cafe_id)
            
            delete = st.button("Delete Cafe")
            if delete:
                cafes.delete(cafe_id)
                st.rerun()