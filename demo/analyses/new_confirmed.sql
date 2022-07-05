with newly_confirmed_cases as (
     select date,
            sum(new_confirmed) confirmed
    from {{ ref('stg_prepared_source') }}
    where date >= {{ dbt_date.today("America/New_York") }} - 3
    group by  date

)

select * from newly_confirmed_cases