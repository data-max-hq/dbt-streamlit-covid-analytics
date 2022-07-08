import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import time
import os
import pycountry as country
import json
import requests
import altair as alt
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
        os.system('dbt seed --profiles-dir ./profiles --target docker')
        time.sleep(1)
    st.success('Seeds successfully inserted!')

    with st.spinner('Building models...'):
        os.system('dbt run --full-refresh --profiles-dir ./profiles  --target docker')
        time.sleep(1)
    st.success('Models built!')

    with st.spinner('Creating tests...'):
        os.system('dbt test --profiles-dir ./profiles  --target docker')
        time.sleep(1)
    st.success('Tests created!')

    time.sleep(0.5)

    st.success('Db populated!')

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

components.html("""
    <style>svg{
        width: 100vw;
        height: 40vh;
        margin-top: 20vh;
        }
        </style>
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 90 13.06"><defs><style>.cls-1{fill:#333;}.cls-2{fill:#f15a24;}</style></defs><g id="Ebene_2" data-name="Ebene 2"><g id="Ebene_1-2" data-name="Ebene 1"><path class="cls-1" d="M11.68,3.33A5.83,5.83,0,0,0,9.22,1.08,8,8,0,0,0,5.59.29H0V13.06H5.59a8,8,0,0,0,3.63-.79A5.83,5.83,0,0,0,11.68,10a6.26,6.26,0,0,0,.88-3.34A6.27,6.27,0,0,0,11.68,3.33ZM9.59,9A3.82,3.82,0,0,1,8,10.52a5.41,5.41,0,0,1-2.47.54H2.37V2.29H5.48A5.41,5.41,0,0,1,8,2.83,3.82,3.82,0,0,1,9.59,4.37a4.45,4.45,0,0,1,.58,2.31A4.44,4.44,0,0,1,9.59,9Z"/><polygon class="cls-2" points="61.42 0.29 56.44 8.76 51.37 0.29 49.41 0.29 49.41 13.06 51.68 13.06 51.68 4.7 55.88 11.6 56.93 11.6 61.13 4.59 61.15 13.06 63.4 13.06 63.38 0.29 61.42 0.29"/><polygon class="cls-2" points="85.2 6.46 89.67 0.29 87.1 0.29 83.87 4.83 80.6 0.29 77.92 0.29 82.41 6.55 78.44 12 71.29 0 64.25 13.06 66.95 13.06 71.39 4.66 73.63 8.43 71.27 8.43 70.19 10.48 74.85 10.48 73.98 9.01 75.03 10.77 75.02 10.77 76.46 13.06 79.07 13.06 79.07 13.06 80.36 13.06 83.79 8.21 87.26 13.06 90 13.06 85.2 6.46"/><polygon class="cls-1" points="36.7 0.29 24.59 0.29 24.59 2.29 28.82 2.29 28.82 13.06 31.2 13.06 31.2 2.29 35.43 2.29 36.7 0.29"/><polygon class="cls-1" points="12.08 13.06 14.79 13.06 19.22 4.66 21.46 8.43 19.1 8.43 18.02 10.48 22.69 10.48 22.86 10.77 22.86 10.77 24.3 13.06 26.9 13.06 19.12 0 12.08 13.06"/><polygon class="cls-1" points="33.17 13.06 35.88 13.06 40.32 4.66 42.56 8.43 40.2 8.43 39.11 10.48 43.78 10.48 43.95 10.77 43.95 10.77 45.39 13.06 48 13.06 40.22 0 33.17 13.06"/></g></g></svg>
""")

country_samples = []
country_codes = []

for c in country.countries:
    # Get names and country codes for all ISO:3166 countries
    country_samples.append(c.name)
    country_codes.append(c.alpha_2)

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

if get_data:
    populate_db(selection_codes)
    dataframe = pd.read_sql_table('covid_data', con=engine, schema='public_source')
    st.write(dataframe)
    chart = pd.read_sql_table('stg_deaths_per_month', con=engine)
    alt_chart = alt.Chart(chart).mark_line().encode(
        x = alt.X('month_year', title='Month'),
        y = alt.Y('deaths', title='Number of Deaths'),
        color = alt.Color('code', title='Countries')
    )
    st.altair_chart(alt_chart, use_container_width=True)
