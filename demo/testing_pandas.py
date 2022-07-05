import pandas as pd
from sqlalchemy import create_engine
import emoji
engine = create_engine('postgresql://postgres:postgres@localhost:5432/postgres')


# i.to_sql('Stat_Table',engine,if_exists='replace')


df = pd.read_sql_query('select * from "fct_day_evaluation"',con=engine)

df['icons'] = df['day_evaluation'].apply(lambda x: emoji.emojize(x,language='alias'))


print(df.head())