with  country_data as (

    select distinct b.name,
           b.code,
           a.region,
           a.sub_region,
           a.intermediate_region,
           b.population
    from {{ ref('stg_country_data')}} as a
    join {{ source('source', 'covid_data') }} as b
    on a.code=b.code
)
select * from country_data