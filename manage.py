#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    if os.environ.get('TIME_TRAVEL'):
        import time_machine

        time_destination = os.environ.get('TIME_TRAVEL')  # get the destination (as a date string)
        print("travelling into time at", time_destination)
        with time_machine.travel(time_destination):
            main()
    else:
        main()
