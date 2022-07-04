{% macro calc_death_rate(n=4) %}
    (a.deaths/b.population)*{{10**n}}
{% endmacro%}