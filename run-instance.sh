#!/usr/bin/bash

# Generate documentation (if needed)
# ~/.cache/pypoetry/virtualenvs/`~/.local/bin/poetry poetry env list --full-path | head -n1 | cut -d " " -f 1`bin/python runserver make_docs

echo "using "`~/.local/bin/poetry env list --full-path | head -n1 | cut -d " " -f 1`

# Deploy statics
`~/.local/bin/poetry env list --full-path | head -n1 | cut -d " " -f 1`/bin/python manage.py collectstatic --no-input

# Run gunicorn workers
exec `~/.local/bin/poetry env list --full-path | head -n1 | cut -d " " -f 1`/bin/gunicorn --workers 2 --log-file ../log/gunicorn_django.log -b unix:$HOME/biomaid.sock dra.wsgi
