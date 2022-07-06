Welcome to your new dbt project!


# covid-dbt-analytics
Dbt project with postgres, python, and streamlit.
<hr>

## Requirements
* Python
* dbt-core & dbt-postgres
* Docker Compose
* The Office (American TV series)

# Run the dbt project without streamlit

## Start the database container
```bash
docker compose up postgres
```
This will create a postgres container from the image defined in the docker-compose.yaml file.



## Connect to the database
Using your favourite SQL IDE, create a new connection with a Postgres database instance.

```
Credentials:

host: localhost
database: postgres
username: postgres
password: postgres
port: 5432
```

## Install dependencies
```bash
pip install -r requirements.txt
```
Make sure you are using a virtual environment for this. 


## Install dbt packages 
```bash
cd demo
dbt deps
```
From now on every other command will have a prefix of 'dbt', so be prepared to ruin those three keyboard keys.

By "three keys" I mean <kbd>Ctrl</kbd> + <kbd>C</kbd> and <kbd>Ctrl</kbd> + <kbd>V</kbd>  🤓


## Get data from the API
There is python script that reads from  https://corona-api.com/countries/{country_code}?includeTimeline=True and writes in <i>covid_data.csv</i> in the <b>seeds</b> folder.

E.g.  https://corona-api.com/countries/al?includeTimeline=True

An example of the JSON response is as follows. The <b>data.timeline</b> list is what feeds the <i>covid_data</i> table with records.

```
{
   "data":{
      "coordinates":{
         "latitude":41,
         "longitude":20
      },
      "name":"Albania",
      "code":"AL",
      "population":2986952,
      "updated_at":"2022-07-06T08:12:23.204Z",
      "today":{
         "deaths":0,
         "confirmed":0
      },
      "latest_data":{
         "deaths":2619,
         "confirmed":166690,
         "recovered":151914,
         "critical":12157,
         "calculated":{
            "death_rate":1.5711800347951288,
            "recovery_rate":91.13564101025857,
            "recovered_vs_death_ratio":null,
            "cases_per_million_population":3
         }
      },
      "timeline":[
         {
            "updated_at":"2022-07-06T04:20:58.000Z",
            "date":"2022-07-06",
            "deaths":3502,
            "confirmed":282690,
            "recovered":0,
            "new_confirmed":0,
            "new_recovered":0,
            "new_deaths":0,
            "active":279188
         }
        ]
      }
   }


```
Run script
```bash
python get_data.py
```


## CSV to database tables
Seeds are CSV files in your dbt project (typically in your seeds directory), that dbt can load into your data warehouse using the <i>dbt seed</i> command.
```bash
dbt seed --profiles-dir ./profiles
```
Refresh the <i>public_source</i> schema of the <i>postgres</i> database to check that both csv-s are converted to database tables.

These are going to be used as the source for the rest of our models.


## Create and update models
Models can be translated as tables or views in the database language. These are called materialization types.
```bash
dbt run  --profiles-dir ./profiles

# To run a specific model use the --select <sql_file_name_of_the_model>
# E.g.:
dbt run  --select stg_country_data --profiles-dir ./profiles
```

## Materialization types
Types: 
* View
* Table
* Ephemeral
* Incremental

Ref: https://docs.getdbt.com/docs/building-a-dbt-project/building-models/materializations

To fully refresh an incremental model use the following command:
```bash
dbt run --full-refresh --profiles-dir ./profiles
```


## Run tests
Tests are SQL queries done to the data. 
Types:
* Singular - built-in
* Generic  - custom tests defined as sql files under the <b>tests</b> folder.
```bash
# Run all tests
dbt test --profiles-dir ./profiles

# Run singular tests
dbt test --select test_type:singular

# Run generic tests 
dbt test --select test_type:generic
```


## Compile analyses
Analysis are sql files  you want to save and version inside of your dbt project but you don't need to materialize them.

```bash
 dbt compile --select analysis --profiles-dir ./profiles
```
Fact:
You can actually just compile models too by replacing 'run' with 'compile' and see the generated sql under the <b>targets</b> folder.

Another fact: Bears eat beets.


## Macros aren't really that big
Just a fancy word for function. In this project they are mainly called within models but they can also be executed separately.
```bash
# dbt run-operation {macro} --args {args}

dbt run-operation run_this_sql --profiles-dir ./profiles
```

## Docs and DAGs
Ref: https://docs.getdbt.com/docs/building-a-dbt-project/documentation
```bash
# Update dbt documents
dbt docs generate --profiles-dir ./profiles

# Check out the documentation and the data flow graph
dbt docs serve --profiles-dir ./profiles
```

## Stop the docker container 
```bash
docker compose down
```

<hr>

# Run the dbt project with streamlit

## Install requirements and create the docker containers

```bash
pip install -r requirements.txt
docker compose up --build
```

## Open the UI
Use a browser to navigate to  http://172.29.0.2:8501

From the UI choose a list of countries you would like so see analytics regarging covid for the past 2-3 years and the output messages will show you the steps followed to generate a line graph for each chosen country.



## Stop the docker container and create your own dbt project 💃
```bash
docker compose down
```


<hr>



### Resources:
- Learn more about dbt [in the docs](https://docs.getdbt.com/docs/introduction)
- Check out [Discourse](https://discourse.getdbt.com/) for commonly asked questions and answers
- Join the [chat](https://community.getdbt.com/) on Slack for live discussions and support
- Find [dbt events](https://events.getdbt.com) near you
- Check out [the blog](https://blog.getdbt.com/) for the latest news on dbt's development and best practices
