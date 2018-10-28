#!/usr/bin/env bash
python3 manage.py migrate
python3 manage.py collectstatic --clear --noinput
python3 manage.py --noinput

touch /src/logs/gunicorn.log
touch /src/logs/access.log
tail -n 0 -f /src/logs/*.log &

echo Starting nginx...
echo Starging Gunicorn...
exec gunicorn Caffein2.wsgi --bind 0.0.0.0:8000 --workers=3

exec service nginx start