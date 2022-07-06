{{ config(materialized='view') }}

with day_evaluation as (

    select date,
           code,
           case when new_recovered > new_deaths then ':smile:'
                 when new_recovered < new_deaths then ':sob:'
                 else ':rocket:'
           end day_evaluation
    from {{ ref('stg_prepared_source')}}


)

select * from day_evaluation


