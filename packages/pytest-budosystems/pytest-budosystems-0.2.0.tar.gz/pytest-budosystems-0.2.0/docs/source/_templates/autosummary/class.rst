{{ fullname | escape | underline }}

.. currentmodule:: {{ module }}

.. autoclass:: {{ objname }}
  :members:
  :inherited-members:
  :undoc-members:

{% block inherited_members %}
  {%- set not_special = inherited_members | rejectattr("0", "eq", "_") | list %}
  {%- if not_special %}
    .. rubric:: {{ _('Inherited Members') }}

    .. hlist::
      :columns: 4
    {% for item in not_special %}
      * {{ item }}
    {%- endfor %}
  {%- endif %}
{%- endblock %}

{#{% block attributes %}#}
{#  {%- if attributes %}#}
{#    .. rubric:: {{ _('Attributes') }}#}
{##}
    {#  .. autosummary:: #}
{#    {% for item in attributes %}#}
{#      ~{{ name }}.{{ item }}#}
{#    .. autoattribute:: {{ item }}#}
{#    {%- endfor %}#}
{#  {%- endif %}#}
{#{%- endblock %}#}
{##}
{#{% block methods %}#}
{#  {%- if methods %}#}
{#    .. rubric:: {{ _('Methods') }}#}
{##}
  {# .. autosummary:: #}
{#    {% for item in methods %}#}
{#      ~{{ name }}.{{ item }}#}
{#    .. automethod:: {{ item }}#}
{#    {%- endfor %}#}
{#  {%- endif %}#}
{#{%- endblock %}#}
