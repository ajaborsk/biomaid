{{ app_name }}

This is a BiomAid application created from a template to show some BiomAid
features.

Once this application directory created, to get a working application,
one must :
- add `'{{ app_name }}'` to the `INSTALLED_APPS` list in `settings/__init__.py` 
- add a include path in `dra/urls.py` :
            `path('<str:url_prefix>/{{ app_name }}/', include('{{ app_name }}.urls')),`

DO NOT USE this template with a custom directory.

{% if app_name != 'demo' %}
You gave a custom app name and it's not 'demo', you MUST rename the
template subdirectory from 'demo' to your app name ({{ app_name }}).
{% endif %}
