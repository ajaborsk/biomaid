#!/usr/bin/bash

# ensure we are in the biomaid folder
cd $HOME/biomaid

# Add ~/.local/bin to $PATH since poetry lives there
export PATH=$HOME/.local/bin:$PATH

POSITIONAL_ARGS=()

while [[ $# -gt 0 ]]; do
  case $1 in
    -d|--make-docs)
      MAKE_DOCS=TRUE
      shift # past argument
      ;;
    -s|--install-statics)
      INSTALL_STATICS=TRUE
      shift # past argument
      ;;
    -r|--reset-to-demo)
      RESET_DEMO=TRUE
      shift # past argument
      ;;
    -*|--*)
      echo "Unknown option $1"
      exit 1
      ;;
    *)
      POSITIONAL_ARGS+=("$1") # save positional arg
      shift # past argument
      ;;
  esac
done

set -- "${POSITIONAL_ARGS[@]}" # restore positional parameters

if [[ $RESET_DEMO = "TRUE" ]]; then
    # Deploy statics
    poetry run python manage.py reset_db --no-input
    poetry run python manage.py migrate
    poetry run python manage.py loaddata fixtures/demo_db.json
fi


if [[ $# -eq 0 ]]; then
    # No argument ==> Run gunicorn workers

    if [[ $MAKE_DOCS = "TRUE" ]]; then
        # Generate documentation (if needed)
        poetry run python manage.py make_docs
    fi

    if [[ $INSTALL_STATICS = "TRUE" ]]; then
        # Deploy statics
        poetry run python manage.py collectstatic --no-input
    fi

    exec poetry run gunicorn --workers 2 --log-file ../log/gunicorn_django.log -b unix:$HOME/biomaid.sock dra.wsgi
else
    # Run the provided commands 
    exec poetry run python manage.py $*
fi
