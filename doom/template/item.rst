{{ module }}
{{ under_line(module, '=') }}

{% for name, command in name_cls.iteritems() %}
{{ module }}.{{ name }}
{{ under_line(module + '.' + name, '-') }}

.. autoclass:: {{ module_path_prefix }}.{{ module }}{{ command }}
    :members:
{% endfor %}