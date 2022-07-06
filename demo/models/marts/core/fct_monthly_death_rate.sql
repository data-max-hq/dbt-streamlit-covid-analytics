{%  set n = 2 %}
with monthly_death_rate as (
    select  dc.name,
            dpm.month_year,
            {{ calc_death_rate(n) }} death_rate,
            power(10, {{ n }}) as per_num_of_people
    from {{ ref('stg_deaths_per_month')}} dpm
    join {{ ref('dim_countries')}} dc
    on dpm.code=dc.code
)

select * from monthly_death_rate



