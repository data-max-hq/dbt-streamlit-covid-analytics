{{ config(materialized='incremental',unique_key=['code','_year']) }}

with stg_deaths_per_year as (
select code,
       to_char(date, 'YYYY') as _year,
	   sum(new_deaths) deaths

from {{ ref('stg_prepared_source') }}

{% if is_incremental() %}

  -- this filter will only be applied on an incremental run
--  where month_year >= (select max(month_year) from {{ this }})

{% endif %}

group by code, _year
)

select * from stg_deaths_per_year