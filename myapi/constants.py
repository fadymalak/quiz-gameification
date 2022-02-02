
TEMPLATE =  '''{% firstof exception_type 'Report' %}{% if request %} at {{ request.path_info }}{% endif %}
{% firstof exception_value No exception message supplied %}
{% if request %}
Request Method: {{ request.META.REQUEST_METHOD }}
Request URL: {{ url }}{% endif %}
Django Version: {{ django_version_info }}
Server time: {{server_time|date:"r"}}
{% if user_str %}USER: {{ user_str }}{% endif %}
{% if raising_view_name %}Raised during: {{ raising_view_name }}{% endif %}

Traceback (most recent call last):
{% for frame in frames %}{% ifchanged frame.exc_cause %}{% if frame.exc_cause %}
{% if frame.exc_cause_explicit %}The above exception ({{ frame.exc_cause }}) was the direct cause of the following exception:{% else %}During handling of the above exception ({{ frame.exc_cause }}), another exception occurred:{% endif %}
{% endif %}{% endifchanged %} 
{% if frame.tb %} [*] "{{ frame.filename  }}"{% if frame.context_line %}, line {{ frame.lineno }}{% endif %}, in {{ frame.function }}
{% if frame.context_line %}    {% spaceless %}{{ frame.context_line }}{% endspaceless %}{% endif %}{% else %}{% if forloop.first %}None{% else %}Traceback: None{% endif %}{% endif %}
{% endfor %}

data :
{%for k ,v in data %}-> {{ k }} : {{ v  }}
{% endfor %}

'''