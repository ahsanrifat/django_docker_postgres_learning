#!/bin/sh
if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DB_HOST $DB_PORT; do
      sleep 0.1
    done

    echo "PostgreSQL started"
fi

python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput
echo "from django.contrib.auth import get_user_model;
admin=get_user_model().objects.filter(email='$DJANGO_ADMIN_EMAIL');
if not admin:
  print('Creating Admin')
  get_user_model().objects.create_superuser('$DJANGO_ADMIN_EMAIL', '$DJANGO_ADMIN_PASSWORD')
else:
  print('Admin registered already')
  print(admin[0])
  " | python manage.py shell

exec "$@"