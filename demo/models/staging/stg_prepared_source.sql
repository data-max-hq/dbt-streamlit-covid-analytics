with stg_prepared_source as (

    select * from {{ source('source', 'covid_data') }}
),

final as (

    select date,
           code,
           sum(deaths) deaths,
           sum(confirmed) confirmed,
           sum(recovered) recovered,
           sum(new_confirmed) new_confirmed,
           sum(new_recovered) new_recovered,
           sum(new_deaths) new_deaths
    from stg_prepared_source
    group by date, code
    order by date
)

select * from final