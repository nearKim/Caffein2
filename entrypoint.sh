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
export EMAIL_HOST_PASSWORD="$(aws ssm get-parameters \
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
export LEGACY_NAVER_CLIENT_ID="$(aws ssm get-parameters \
                            --region ${REGION} \
                            --name /prod/naver/legacy_client_id \
                            | jq -r '.Parameters | .[] | .Value')"
export LEGACY_NAVER_CLIENT_SECRET="$(aws ssm get-parameters \
                            --region ${REGION} \
                            --with-decryption \
                            --name /prod/naver/legacy_client_secret \
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
export FACEBOOK_APP_TOKEN_60="$(aws ssm get-parameters \
                            --region ${REGION} \
                            --with-decryption \
                            --name /prod/facebook/app_token_60 \
                            | jq -r '.Parameters | .[] | .Value')"

echo Environment Variable register complete.....


echo Now make Django work......
python3 manage.py migrate
echo Migration Complete......

echo Collect static......
python3 manage.py collectstatic --clear --noinput
python3 manage.py collectstatic --noinput
echo Collect static Complete

touch /srv/logs/gunicorn.log
touch /srv/logs/access.log
tail -n 0 -f /srv/logs/*.log &

echo Starting nginx...
echo Starting Gunicorn...
exec gunicorn Caffein2.wsgi --bind 0.0.0.0:8000 --workers=3

exec service nginx start
