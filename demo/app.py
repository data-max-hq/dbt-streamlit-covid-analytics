import streamlit as st
import pandas as pd
import time
import os
import pycountry as country
import json
import requests
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:postgres@localhost:5433/postgres')

def populate_db(countries):
    st.write('Creating the seeds...')
    with st.spinner('Wait for it...'):
        create_seeds(countries)
        time.sleep(1)
    st.success('Seeds successfully created!')

    st.write('Installing dependencies...')
    with st.spinner('Wait for it...'):
        os.system('dbt deps')
        time.sleep(1)
    st.success('Dependencies successfully installed!')

    st.write('Populating db...')
    with st.spinner('Wait for it...'):
        os.system('dbt seed --profiles-dir ./profiles')
        time.sleep(1)
    st.success('Seeds successfully inserted!')

    with st.spinner('Wait for it...'):
        os.system('dbt run --full-refresh --profiles-dir ./profiles')
        time.sleep(1)
    st.success('Models built!')

    with st.spinner('Wait for it...'):
        os.system('dbt test --profiles-dir ./profiles')
        time.sleep(1)
    st.success('Tests created!')

    time.sleep(0.5)

    st.success('Db populated!')

def set_false(button):
    button = False

def create_seeds(countries):
    df_main = None

    for c_code in countries:
        url = f"https://corona-api.com/countries/{c_code}?includeTimeline=True"
        response = requests.request("GET", url)
        data = json.loads(response.text)
        timeline = data['data']['timeline']
        df = pd.DataFrame(timeline)
        df["name"] = data['data']['name']
        df["code"] = data['data']['code']
        df["population"] = data['data']['population']
        df_main = pd.concat([df_main, df]) if df_main is not None else df

    df_main.to_csv(f'seeds/covid_data.csv', index=False)



country_samples = []
country_codes = []
for i in range(0,20):
    country_samples.append(list(country.countries)[i].name)
    country_codes.append(list(country.countries)[i].alpha_2)
st.write('# *DBT Visualisation App*')
populate = st.button('Populate DB', 1, 'Populate the database', disabled=True)
remove = st.button('Remove Output', 2, disabled=False)

if populate:
    populate_db(country_codes)

selection = st.multiselect('Select countries: ', country_samples)

selection_codes = []

for name in selection:
    selection_codes.append(country_codes[country_samples.index(name)])

get_data = st.button('Get Data', 3, 'Get data for the countries selected')

if remove:
    set_false(get_data)

if get_data:
    populate_db(selection_codes)
    dataframe = pd.read_sql_table('covid_data', con=engine, schema='public_source')
    st.write(dataframe)
country_samples = []
for i in range(0,20):
    country_samples.append(list(country.countries)[i].name)
st.write('# *DBT Visualisation App*')
populate = st.button('Populate DB', 1, 'Populate the database', on_click=populate_db)
remove = st.button('Remove Output', 2)


st.multiselect('Select countries: ', country_samples)
