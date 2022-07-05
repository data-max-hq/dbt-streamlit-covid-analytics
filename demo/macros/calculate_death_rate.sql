{% macro calc_death_rate(n=4) %}

    (dpm.deaths/dc.population) * {{ 10**n }}

{% endmacro%}