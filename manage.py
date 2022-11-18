#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging


def main():
    """Run administrative tasks."""
    logging.basicConfig(format='[%(asctime)s] %(levelname)s:%(message)s', datefmt='%d/%b/%Y %H:%M:%S',
                        filename='EPIC_Events.log', encoding='utf-8', level=logging.INFO)
    logging.info('Started server')
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'epic.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)
    logging.info('Stopped server')


if __name__ == '__main__':
    main()
