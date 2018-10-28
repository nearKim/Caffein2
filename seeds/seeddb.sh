#!/bin/sh
echo 'Seed initial DB with user, activeuser, os data...'

echo 'Seeding user...'
python manage.py loaddata ./accounts.user.json &&
echo 'Seeding activeuser...'
python manage.py loaddata ./accounts.activeuser.json &&
echo 'Seeding partners...'
python manage.py loaddata ./partners.json &&
echo 'Seeding core...'
python manage.py loaddata ./core.json &&
echo 'Seeding sites...'
python manage.py loaddata ./sites.json &&
echo 'Seeding surveys...'
python manage.py loaddata ./surveys.json

echo 'Done seeding.'