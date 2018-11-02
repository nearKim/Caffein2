#!/usr/bin/env bash
REGION="ap-northeast-2"

echo Register Environment variables.......
echo You need to add AWS role to this EC2 instance worker......

$(aws ssm get-parameters-by-path \
            --region ${REGION}\
            --with-decryption \
            --path /prod/aws/credential \
            | jq -r '.Parameters | .[] |"export "  + .Name[21:] +"="+ .Value')

export RDS_PASS="$(aws ssm get-parameters \
                            --region ${REGION} \
                            --with-decryption \
                            --name /prod/aws/rds_pass \
                            | jq -r '.Parameters | .[] | .Value')"

export SECRET_KEY="$(aws ssm get-parameters \
                            --region ${REGION} \
                            --with-decryption \
                            --name /prod/django/secret_key \
                            | jq -r '.Parameters| .[] | .Value')"
export GMAIL_PASS="$(aws ssm get-parameters \
                            --region ${REGION} \
                            --with-decryption \
                            --name /prod/google/gmail_pass \
                            | jq -r '.Parameters | .[] | .Value')"
export NAVER_CLIENT_ID="$(aws ssm get-parameters \
                            --region ${REGION} \
                            --name /prod/naver/client_id \
                            | jq -r '.Parameters | .[] | .Value')"
export NAVER_CLIENT_SECRET="$(aws ssm get-parameters \
                            --region ${REGION} \
                            --with-decryption \
                            --name /prod/naver/client_secret \
                            | jq -r '.Parameters | .[] |  .Value')"
export FACEBOOK_APP_ID="$(aws ssm get-parameters \
                            --region ${REGION} \
                            --name /prod/facebook/app_id \
                            | jq -r '.Parameters | .[] | .Value')"
export FACEBOOK_APP_SECRET="$(aws ssm get-parameters \
                            --region ${REGION} \
                            --with-decryption \
                            --name /prod/facebook/app_secret \
                            | jq -r '.Parameters | .[] | .Value')"
export FACEBOOK_APP_TOKEN="$(aws ssm get-parameters \
                            --region ${REGION} \
                            --with-decryption \
                            --name /prod/facebook/app_token_60 \
                            | jq -r '.Parameters | .[] | .Value')"

echo Environment Variable register complete.....


echo Now make Django work......
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