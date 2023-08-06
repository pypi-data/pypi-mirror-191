{{ fullname | escape | underline }}

.. automodule:: {{ fullname }}
{%- set exclude = (classes if classes else []) + (exceptions if exceptions else []) %}
{%- if exclude %}
    :exclude-members: {{ exclude|join(", ") }}
{% endif %}

{% block attributes %}
  {%- if attributes %}
    .. rubric:: {{ _('Module Attributes') }}

    .. autosummary::
    {% for item in attributes %}
      {{ item }}
    {%- endfor %}
  {%- endif %}
{%- endblock %}

{% block data %}
  {%- if data %}
    .. rubric:: {{ _('Module Data') }}

    .. autosummary::
    {% for item in data %}
      {{ item }}
    {%- endfor %}
  {%- endif %}
{%- endblock %}

{% block functions %}
  {%- if functions %}
    .. rubric:: {{ _('Functions') }}

    .. autosummary::
    {% for item in functions %}
      {{ item }}
    {%- endfor %}
  {%- endif %}
{%- endblock %}

{% block classes %}
  {%- if classes %}
    .. rubric:: {{ _('Classes') }}

    .. autosummary::
      :toctree:
    {% for item in classes %}
      {{ item }}
    {%- endfor %}
  {%- endif %}
{%- endblock %}

{% block exceptions %}
  {%- if exceptions %}
    .. rubric:: {{ _('Exceptions') }}

    .. autosummary::
      :toctree:
    {% for item in exceptions %}
      {{ item }}
    {%- endfor %}
  {%- endif %}
{%- endblock %}

{% block modules %}
  {%- if modules %}
    .. rubric:: Modules

    .. autosummary::
      :recursive:
      :toctree:
    {% for item in modules %}
      {{ item }}
    {%- endfor %}
  {%- endif %}
{%- endblock %}
