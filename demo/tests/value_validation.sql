select *
from {{ ref('stg_prepared_source')}}
where confirmed < new_confirmed