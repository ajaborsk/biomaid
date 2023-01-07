#!/usr/bin/bash

# Generate documentation (if needed)
# ~/.cache/pypoetry/virtualenvs/`~/.local/bin/poetry env list`/bin/python runserver make_docs

# Deploy statics
~/.cache/pypoetry/virtualenvs/`~/.local/bin/poetry env list`/bin/python runserver collectstatic

# Run gunicorn workers
~/.cache/pypoetry/virtualenvs/`~/.local/bin/poetry env list`/bin/gunicorn --workers 4 --log-file ../log/gunicorn_django.log -b unix:/run/biomaid/$USER.sock dra.wsgi
