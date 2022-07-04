{{ config(materialized='incremental',unique_key=['code','month_year']) }}

with stg_deaths_per_month as (
select code,
       to_char(date, 'YYYY-MM') as month_year,
	   sum(new_deaths) deaths

from {{ ref('stg_prepared_source') }}

{% if is_incremental() %}

  -- this filter will only be applied on an incremental run
--  where month_year >= (select max(month_year) from {{ this }})

{% endif %}

group by code, month_year
)

select * from stg_deaths_per_month