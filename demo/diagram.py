from diagrams import Diagram, Cluster
from diagrams.custom import Custom
from diagrams.onprem.container import Docker
from diagrams.onprem.database import Postgresql

with Diagram("dbt only", show=False, filename="dbt_diagram", direction="LR", curvestyle='curved'):
    with Cluster(""):
        results = [Custom("Tables", "./resources/database-table.jpg")]
        dbt = Custom("dbt", "./resources/dbt-logo.png")
        api = Custom("Source", "./resources/api.png")
        db = Postgresql("PostgreSQL")
        api >> dbt >> db >> results
        Docker("Docker") >> db

with Diagram("dbt with Streamlit", show=False, filename="dbt_streamlit_diagram", direction="LR", curvestyle='curved'):
    with Cluster("App"):
        docker = Docker("Docker")
        db = Postgresql("PostgreSQL")
        streamlit = Custom("Streamlit", "./resources/streamlit.png")
        ui = Custom("Dashboard", "./resources/ui.png")
        dbt = Custom("dbt", "./resources/dbt-logo.png")
        results = Custom("Tables", "./resources/database-table.jpg")
        api = Custom("Source", "./resources/api.png")
        docker >> streamlit >> ui
        docker >> db
        api >> streamlit >> dbt >> db >> results

