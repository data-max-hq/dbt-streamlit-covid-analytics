import streamlit as st
import pandas as pd
import time
import os
import pycountry as country
import json
import requests
from sqlalchemy import create_engine

engine = create_engine('postgresql://postgres:postgres@host.docker.internal:5432/postgres')

def populate_db(countries):
    with st.spinner('Creating the seeds...'):
        create_seeds(countries)
        time.sleep(1)
    st.success('Seeds successfully created!')

    with st.spinner('Installing dependencies...'):
        os.system('dbt deps')
        time.sleep(1)
    st.success('Dependencies successfully installed!')

    st.write('Populating db...')
    with st.spinner('Inserting seeds...'):
        os.system('dbt seed --profiles-dir ./profiles')
        time.sleep(1)
    st.success('Seeds successfully inserted!')

    with st.spinner('Building models...'):
        os.system('dbt run --full-refresh --profiles-dir ./profiles')
        time.sleep(1)
    st.success('Models built!')

    with st.spinner('Creating tests...'):
        os.system('dbt test --profiles-dir ./profiles')
        time.sleep(1)
    st.success('Tests created!')

    time.sleep(0.5)

    st.success('Db populated!')

def set_false(button):
    button = False

def create_seeds(countries):
    df_main = None

    for country_code in countries:
        url = f"https://corona-api.com/countries/{country_code}?includeTimeline=True"
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
    # Get names and country codes for 20 countries
    country_samples.append(list(country.countries)[i].name)
    country_codes.append(list(country.countries)[i].alpha_2)

st.write('# *DBT Visualisation App*')
selection = st.multiselect('Select countries: ', country_samples)

# Find country codes for the countries selected
selection_codes = []
for name in selection:
    selection_codes.append(country_codes[country_samples.index(name)])

col1, col2, col3, col4, col5, col6 = st.columns(6)
with col1:
    get_data = st.button('Get Data', 1, 'Get data for the countries selected')
with col2:
    clear = st.button('Clear', 2)

if clear:
    set_false(get_data)

if get_data:
    populate_db(selection_codes)
    dataframe = pd.read_sql_table('covid_data', con=engine, schema='public_source')
    st.write(dataframe)
