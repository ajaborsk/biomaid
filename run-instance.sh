#!/usr/bin/bash

# VENV_BIN = `~/.local/bin/poetry env list --full-path | head -n1 | cut -d " " -f 1`/bin
# MANAGE_PY_CMD = $VENV_BIN/python manage.py

# Generate documentation (if needed)
# ~/.cache/pypoetry/virtualenvs/`~/.local/bin/poetry poetry env list --full-path | head -n1 | cut -d " " -f 1`bin/python runserver make_docs

# echo "using python virtualenv: "$VENV_BIN

# Deploy statics
poetry run python manage.py collectstatic --no-input

# Run gunicorn workers
exec poetry run gunicorn --workers 2 --log-file ../log/gunicorn_django.log -b unix:$HOME/biomaid.sock dra.wsgi
