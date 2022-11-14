import os
from time import sleep
import requests
import json

import pandas as pd

COUNTRIES_PATH = os.path.join("seeds", "countries.csv")
COVID_DATA_PATH = os.path.join("seeds", "covid_data.csv")
RAW_COLUMNS =  ["Country", "Confirmed", "Deaths", "Recovered", "Active", "Date"]

def parse_countries():
    with open(os.path.join("api_utils", "countries.json"), "r") as file:
        countries = json.load(file)
    df = pd.DataFrame(countries)
    df.columns = [col.lower() for col in df.columns]
    df.to_csv(COUNTRIES_PATH, index=False)

def prepare_template_file():
    columns = [col.lower() for col in RAW_COLUMNS]
    pd.DataFrame(columns=columns).to_csv(COVID_DATA_PATH, index=False)

def get_country_data(country):
    response = requests.get(f"https://api.covid19api.com/total/country/{country}")
    if response.status_code != 200:
        raise Exception(f"Failure in downloading data for {country}.\nReason: {response.reason}")

    # save API results
    os.makedirs(os.path.join("api_utils", country), exist_ok=True)
    with open(os.path.join("api_utils", country, f"{country}.json"), "w") as file:
        json.dump(response.json(), file)

    country_df = pd.DataFrame(response.json())[RAW_COLUMNS]
    country_df.columns = [col.lower() for col in country_df.columns]

    all_available_countries_df = pd.read_csv(COVID_DATA_PATH)
    all_available_countries_df = pd.concat([country_df, all_available_countries_df], axis=0).drop_duplicates()

    all_available_countries_df.to_csv(COVID_DATA_PATH, index=False)


if __name__ == "__main__":
    if not os.path.isfile(COUNTRIES_PATH):
        parse_countries()

    if not os.path.isfile(COVID_DATA_PATH):
        prepare_template_file()

    # download example countries
    example_countries = ("poland", "germany")
    for country in example_countries:
        get_country_data(country)
        sleep(10)
