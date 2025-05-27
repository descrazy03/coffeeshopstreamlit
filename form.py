import streamlit as st
from controller import Controller
from database.models import CafeBase
from datetime import datetime

cafes = Controller("cafes")

# ''' Define forms for adding and updating values in database tables '''


def cafe_form(cafe_id=None):

    with st.form(("update" if cafe_id != None else "add") + " cafe", border=False, clear_on_submit=True):
        if cafe_id != None:
            og = cafes.get_one(cafe_id)
        st.header("Cafe Information")
        name_input = st.text_input("Cafe Name:", value="" if cafe_id == None else og['name'].iloc[0])
        address_input = st.text_input("Cafe Address: ", value="" if cafe_id == None else og['address'].iloc[0])
        has_restroom_input = st.checkbox("Has Restroom", value=False if cafe_id == None else og['has_restroom'].iloc[0])
        restroom_pass_input = st.text_input("Restroom Password: ", value="" if cafe_id == None else og['restroom_pass'].iloc[0])
        has_wifi_input = st.checkbox("Has Wifi", value=False if cafe_id == None else og['has_wifi'].iloc[0])
        wifi_pass_input = st.text_input("Wifi Password: ", value="" if cafe_id == None else og['wifi_pass'].iloc[0])
        has_outlets_input = st.checkbox("Has Outlets", value=False if cafe_id == None else og['has_outlets'].iloc[0])
        is_fav_input = st.checkbox("Recommended for Work", value=False if cafe_id == None else og['is_fav'].iloc[0])
        notes_input = st.text_area("Additional Notes", value="" if cafe_id == None else og['notes'].iloc[0])
        
        st.header("Hours Information")
        st.subheader("Monday")
        monday_open = st.time_input("Monday Opening Hours: ",value=None if (cafe_id == None) or (og['mon_open'].iloc[0] == "") else og['mon_open'].iloc[0])
        monday_close = st.time_input("Monday Closing Hours: ", value=None if (cafe_id == None) or (og['mon_close'].iloc[0] == "") else og['mon_close'].iloc[0])
        st.subheader("Tuesday")
        tuesday_open = st.time_input("Tuesday Opening Hours: ", value=None if (cafe_id == None) or (og['tue_open'].iloc[0] == "") else og['tue_open'].iloc[0])
        tuesday_close = st.time_input("Tuesday Closing Hours: ", value=None if (cafe_id == None) or (og['tue_close'].iloc[0] == "") else og['tue_close'].iloc[0])
        st.subheader("Wednesday")
        wednesday_open = st.time_input("Wednesday Opening Hours: ", value=None if (cafe_id == None) or (og['wed_open'].iloc[0] == "") else og['wed_open'].iloc[0])
        wednesday_close = st.time_input("Wednesday Closing Hours: ", value=None if (cafe_id ==None) or (og['wed_close'].iloc[0] == "") else og['wed_close'].iloc[0])
        st.subheader("Thursday")
        thursday_open = st.time_input("Thursday Opening Hours: ", value=None if (cafe_id == None) or (og['thu_open'].iloc[0] == "") else og['thu_open'].iloc[0])
        thursday_close = st.time_input("Thursday Closing Hours: ", value=None if (cafe_id == None) or (og['thu_close'].iloc[0] == "") else og['thu_close'].iloc[0])
        st.subheader("Friday")
        friday_open = st.time_input("Friday Opening Hours: ", value=None if (cafe_id == None) or (og['fri_open'].iloc[0] == "") else og['fri_open'].iloc[0])
        friday_close = st.time_input("Friday CLosing Hours: ", value=None if (cafe_id == None) or (og['fri_close'].iloc[0] == "") else og['fri_close'].iloc[0])
        st.subheader("Saturday")
        saturday_open = st.time_input("Saturday Opening Hours: ", value=None if (cafe_id == None) or (og['sat_open'].iloc[0] == "") else og['sat_open'].iloc[0])
        saturday_close = st.time_input("Saturday Closing Hours: ", value=None if (cafe_id == None) or (og['sat_close'].iloc[0] == "") else og['sat_close'].iloc[0])
        st.subheader("Sunday")
        sunday_open = st.time_input("Sunday Opening Hours: ", value=None if (cafe_id == None) or (og['sun_open'].iloc[0] == "") else og['sun_open'].iloc[0])
        sunday_close = st.time_input("Sunday Closing Hours: ", value=None if (cafe_id == None) or (og['sun_close'].iloc[0] == "") else og['sun_close'].iloc[0])

        submit = st.form_submit_button(("Update" if cafe_id != None else "Add") + " Cafe")
        if submit:
            data = CafeBase(name=name_input if cafe_id == None else name_input.replace("'","''"),
                            address=address_input if cafe_id == None else address_input.replace("'","''"),
                            has_restroom=has_restroom_input,
                            restroom_pass=restroom_pass_input if cafe_id == None else restroom_pass_input.replace("'","''"),
                            has_wifi=has_wifi_input,
                            wifi_pass=wifi_pass_input if cafe_id == None else wifi_pass_input.replace("'","''"),
                            has_outlets=has_outlets_input,
                            notes=notes_input if cafe_id == None else notes_input.replace("'","''"),
                            is_fav=is_fav_input,
                            mon_open=monday_open.strftime("%H:%M") if monday_open != None else "",
                            mon_close=monday_close.strftime("%H:%M") if monday_close != None else "",
                            tue_open=tuesday_open.strftime("%H:%M") if tuesday_open != None else "",
                            tue_close=tuesday_close.strftime("%H:%M") if tuesday_close != None else "",
                            wed_open=wednesday_open.strftime("%H:%M") if wednesday_open != None else "",
                            wed_close=wednesday_close.strftime("%H:%M") if wednesday_close != None else "",
                            thu_open=thursday_open.strftime("%H:%M") if thursday_open != None else "",
                            thu_close=thursday_close.strftime("%H:%M") if thursday_close != None else "",
                            fri_open=friday_open.strftime("%H:%M") if friday_open != None else "",
                            fri_close=friday_close.strftime("%H:%M") if friday_close != None else "",
                            sat_open=saturday_open.strftime("%H:%M") if saturday_open != None else "",
                            sat_close=saturday_close.strftime("%H:%M") if saturday_close != None else "",
                            sun_open=sunday_open.strftime("%H:%M") if sunday_open != None else "",
                            sun_close=sunday_close.strftime("%H:%M") if sunday_close != None else "",
                            updated_at=datetime.now().strftime(format="%m/%d/%y"))
            if cafe_id == None:
                cafes.post(data)
                st.rerun()
            else:
                cafes.update(data, cafe_id)
                st.rerun()