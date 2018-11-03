#!/bin/sh
echo 'Seed initial DB with user, activeuser, os data...'

echo 'Seeding user...'
python3 manage.py loaddata ./accounts.user.json &&
echo 'Seeding activeuser...'
python3 manage.py loaddata ./accounts.activeuser.json &&
echo 'Seeding partners...'
python3 manage.py loaddata ./partners.json &&
echo 'Seeding core...'
python3 manage.py loaddata ./core.json &&
echo 'Seeding sites...'
python3 manage.py loaddata ./sites.json &&
echo 'Seeding surveys...'
python3 manage.py loaddata ./surveys.json

echo 'Done seeding.'