#!/usr/bin/env bash
set -o errexit

pip install -r requirements.txt

cd meu_projeto

python manage.py collectstatic --no-input

python manage.py migrate

python manage.py shell <<EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin')
    print('Superuser admin criado!')
else:
    print('Superuser admin já existe.')
EOF