{%- from "taiga/map.jinja" import server with context %}

from .celery import *
from .common import *

DEBUG = {{ server.get('debug', False) }}
TEMPLATE_DEBUG = DEBUG

SECRET_KEY = "{{ server.secret_key }}"

PUBLIC_REGISTER_ENABLED = False

MEDIA_URL = "{{ server.server_protocol }}://{{ server.server_name }}/media/"
STATIC_URL = "{{ server.server_protocol }}://{{ server.server_name }}/static/"
ADMIN_MEDIA_PREFIX = "{{ server.server_protocol }}://{{ server.server_name }}/static/admin/"

SITES["front"]["domain"] = "{{ server.server_name }}"
SITES["front"]["scheme"] = "{{ server.server_protocol }}"

DEFAULT_FROM_EMAIL = "{{ server.get('mail_from', server.mail.from) }}"
SERVER_EMAIL = DEFAULT_FROM_EMAIL

EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
{%- if server.mail.get('encryption', 'none') == 'tls' %}
EMAIL_USE_TLS = True
EMAIL_USE_SSL = False
{%- endif %}
{%- if server.mail.get('encryption', 'none') == 'ssl' %}
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
{%- endif %}
EMAIL_HOST = "{{ server.mail.get('host', 'localhost') }}"
EMAIL_PORT = {{ server.mail.get('port', '25') }}
{%- if server.mail.get('user', False) %}
EMAIL_HOST_USER = "{{ server.mail.user }}"
EMAIL_HOST_PASSWORD = "{{ server.mail.password }}"
{%- endif %}

DATABASES = {
    'default': {
        {%- if server.database.engine == 'mysql' %}
        'ENGINE': 'django.db.backends.mysql',
        'PORT': '3306',
        'OPTIONS': { 'init_command': 'SET storage_engine=INNODB,character_set_connection=utf8,collation_connection=utf8_unicode_ci', },
        {% else %}
        'ENGINE': 'django.db.backends.postgresql',
        'PORT': '5432',
        {%- endif %}
        'HOST': '{{ server.database.host }}',
        'NAME': '{{ server.database.name }}',
        'PASSWORD': '{{ server.database.password }}',
        'USER': '{{ server.database.user }}'
    }
}

BROKER_URL = 'amqp{% if server.message_queue.get('ssl', False) %}s{% endif %}://{{ server.message_queue.user }}:{{ server.message_queue.password }}@{{ server.message_queue.host }}:{{ server.message_queue.get('port', 5672) }}/{{ server.message_queue.get('virtual_host', '/') }}'
CELERY_RESULT_BACKEND = 'redis://localhost:6379/0'
CELERY_ENABLED = True

{%- for plugin_name, plugin in server.get('plugin', {}).iteritems() %}
{%- if plugin.get('enabled', true) %}
# Plugin {{ plugin_name}}
INSTALLED_APPS += ['{{ plugin_name }}']
{%- for key, value in plugin.get('parameters', {}).get('backend', {}).iteritems() %}
{{ key|upper }} = '{{ value }}'
{%- endfor %}
{%- endif %}
{%- endfor %}

{#-
vim: syntax=jinja
-#}
