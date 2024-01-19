#!/usr/bin/bash
# =============================================================================
# This script is used to launch a BiomAid instance (or a BiomAid command)
# It takes care of the following tasks :
# - get the appropriate virtual environment from Poetry 
# - collects the statics
# - build the docs if needed
# - reset the database to demo database (if asked)
#
# Usage :
#    bash run-instance.sh [-r|--reset-to-demo] [-s|--install-static] 
#                         [-d|--make-docs] [command]
#    
#    If command is omited, then launch *gunicorn* on the ``$HOME/biomaid.sock`` 
#      unix socket. In this case, try to read instance_config.toml and get
#      number of workers from the [gunicorn_settings] section ('workers' key).
#      default to 2 workers.
#
#    If command is provided, launch instance with this command, within the 
#      appropriate virtual environment (aka 'python manage.py *command*...') 
#
# =============================================================================

<<<<<<< Updated upstream
# ------------------------------------------------------------------------------------------------------------
# These functions need bash.
# They have been published by johnraff aka John Crawley (https://asazuke.com/ https://github.com/johnraff)
# on https://forums.bunsenlabs.org/viewtopic.php?id=5570 

# Usage: parse_config <file> [<default array name>]

# If no default array name is given, it defaults to 'config'.
# If there are [section] headers in file, following entries will be
#  put in array of that name.

# Config arrays may exist already and will appended to or overwritten.
# If preexisting array is not associative, function exits with error.
# New arrays will be created as needed, and remain in the environment.
parse_config(){
    [[ -f $1 ]] || { echo "$1 is not a file." >&2;return 1;}
    local -n config_array="${2:-config}"
    declare -Ag ${!config_array} || return 1
    local line key value section_regex entry_regex
    section_regex="^[[:blank:]]*\[([[:alpha:]_][[:alnum:]_-]*)\][[:blank:]]*(#.*)?$"
    entry_regex="^[[:blank:]]*([[:alpha:]_][[:alnum:]_-]*)[[:blank:]]*=[[:blank:]]*('[^']+'|\"[^\"]+\"|[^#[:blank:]]+)[[:blank:]]*(#.*)*$"
    while read -r line
    do
        [[ -n $line ]] || continue
        [[ $line =~ $section_regex ]] && {
            local -n config_array=${BASH_REMATCH[1]}
            declare -Ag ${!config_array} || return 1
            continue
        }
        [[ $line =~ $entry_regex ]] || continue
        key=${BASH_REMATCH[1]}
        value=${BASH_REMATCH[2]#[\'\"]} # strip quotes
        value=${value%[\'\"]}
        config_array["${key}"]="${value}"
    done < "$1"
}

# Usage: parse_config_vars <file>
# No arrays, just read variables individually.
# Preexisting variables will be overwritten.

# parse_config_vars(){
#     [[ -f $1 ]] || { echo "$1 is not a file." >&2;return 1;}
#     local line key value entry_regex
#     entry_regex="^[[:blank:]]*([[:alpha:]_][[:alnum:]_-]*)[[:blank:]]*=[[:blank:]]*('[^']+'|\"[^\"]+\"|[^#[:blank:]]+)[[:blank:]]*(#.*)*$"
#     while read -r line
#     do
#         [[ -n $line ]] || continue
#         [[ $line =~ $entry_regex ]] || continue
#         key=${BASH_REMATCH[1]}
#         value=${BASH_REMATCH[2]#[\'\"]} # strip quotes
#         value=${value%[\'\"]}
#         declare -g "${key}"="${value}"
#     done < "$1"
# }

# ensure we are in the biomaid folder
cd $HOME/biomaid

# Add ~/.local/bin to $PATH since poetry lives there
export PATH=$HOME/.local/bin:$PATH

=======
# ensure we are in the biomaid folder
cd $HOME/biomaid

# Add ~/.local/bin to $PATH since poetry lives there
export PATH=$HOME/.local/bin:$PATH

>>>>>>> Stashed changes
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

<<<<<<< Updated upstream
    if [ -f instance_config.toml ]; then
        parse_config instance_config.toml
    fi
    workers=${gunicorn_settings[workers]:-2}

    exec poetry run gunicorn --workers $workers --log-file ../log/gunicorn_django.log -b unix:$HOME/biomaid.sock dra.wsgi
=======
    exec poetry run gunicorn --workers 2 --log-file ../log/gunicorn_django.log -b unix:$HOME/biomaid.sock dra.wsgi
>>>>>>> Stashed changes
else
    # Run the provided commands 
    exec poetry run python manage.py $*
fi
