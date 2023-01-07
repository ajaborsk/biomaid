#!/usr/bin/bash

# Generate documentation (if needed)
#...

# Deploy static
#...

# Run gunicorn workers
~/.cache/pypoetry/virtualenvs/`~/.local/bin/poetry env list`/bin/gunicorn --workers 4 --log-file ../log/gunicorn_django.log dra.wsgi
