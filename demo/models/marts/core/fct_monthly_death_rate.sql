{%  set n = 2 %}
with monthly_death_rate as (
    select  b.name,
            a.month_year,
            {{calc_death_rate(n)}} death_rate,
            power(10,{{n}}) as per_num_of_people
    from {{ ref('stg_deaths_per_month')}} a
    join {{ ref('dim_countries')}} b
    on a.code=b.code
    --order by a.month_year desc
)

select * from monthly_death_rate



