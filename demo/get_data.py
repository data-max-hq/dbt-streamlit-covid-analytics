import requests
import json
import pandas as pd
import sys

df_main = None
countries = sys.argv[2:]
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