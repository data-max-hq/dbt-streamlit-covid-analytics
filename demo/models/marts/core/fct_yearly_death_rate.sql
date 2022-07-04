with yearly_death_rate as (
    select  b.name,
            a._year,
            {{calc_death_rate()}} death_rate
    from {{ ref('stg_deaths_per_year')}} a
    join {{ ref('dim_countries')}} b
    on a.code=b.code
    --order by a._year desc
)

select * from yearly_death_rate



