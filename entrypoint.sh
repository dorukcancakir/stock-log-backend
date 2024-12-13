#!/bin/bash
python manage.py migrate
python manage.py loaddata core/fixtures/*.json
python manage.py collectstatic --no-input
supervisord -c /etc/supervisor/supervisord.conf