#!/usr/bin/bash

# Generate documentation (if needed)
# ~/.cache/pypoetry/virtualenvs/`~/.local/bin/poetry env list`/bin/python runserver make_docs

# Deploy statics
~/.cache/pypoetry/virtualenvs/`~/.local/bin/poetry env list`/bin/python manage.py collectstatic --no-input

# Run gunicorn workers
exec ~/.cache/pypoetry/virtualenvs/`~/.local/bin/poetry env list`/bin/gunicorn --workers 4 --log-file ../log/gunicorn_django.log -b unix:$HOME/biomaid.sock dra.wsgi
