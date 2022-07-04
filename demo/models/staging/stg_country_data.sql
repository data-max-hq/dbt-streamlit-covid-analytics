with stg_country_data as (

    select
            region,
            {{'"'}}alpha-2{{'"'}} as code,
            {{'"'}}sub-region{{'"'}} as sub_region,
            {{'"'}}intermediate-region{{'"'}} as intermediate_region
    from  {{ source('source', 'countries') }}
    where region is not null

)

select * from stg_country_data