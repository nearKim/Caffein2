#!/bin/sh
echo 'Seed initial DB with user, activeuser, os data...'

echo 'Seeding user...'
python manage.py loaddata ./seeds/accounts.user.json &&
echo 'Seeding activeuser...'
python manage.py loaddata ./seeds/accounts.activeuser.json &&
echo 'Seeding partners...'
python manage.py loaddata ./seeds/partners.json &&
echo 'Seeding core...'
python manage.py loaddata ./seeds/core.json &&
echo 'Seeding sites...'
python manage.py loaddata ./seeds/sites.json &&
echo 'Seeding surveys...'
python manage.py loaddata ./seeds/surveys.json

echo 'Done seeding.'