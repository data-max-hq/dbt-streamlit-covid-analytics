import streamlit as st
import pandas as pd
import time
import os
import pycountry as country

def populate_db():
    st.info('Populating db...')
    
    with st.spinner('Wait for it...'):
        os.system('dbt seed --profiles-dir ./profiles')
        time.sleep(1)
    st.success('Seeds successfully inserted!')
    os.system('dbt run --profiles-dir ./profiles')
    os.system('dbt test --profiles-dir ./profiles')
    st.success('Db populated!')

def set_false(button):
    button = False

country_samples = []
for i in range(0,20):
    country_samples.append(list(country.countries)[i].name)
st.write('# *DBT Visualisation App*')
populate = st.button('Populate DB', 1, 'Populate the database', on_click=populate_db)
remove = st.button('Remove Output', 2)


st.multiselect('Select countries: ', country_samples)



