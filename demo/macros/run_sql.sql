{%  macro run_this_sql() %}
    {% set sql_query  %}

         select code,
               to_char(date, 'YYYY-MM') as month_year,
               sum(new_recovered) recovered


        from {{ref('stg_prepared_source')}}
        group by code, month_year
        order by code, month_year desc

    {% endset  %}

    {% if execute %}

        {%  set result = run_query(sql_query).columns.values() %}
        {{ log('SQL results ---- ' ~ result, info=True) }}


    {%  endif %}

{%  endmacro  %}