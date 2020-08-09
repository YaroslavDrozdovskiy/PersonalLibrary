release: python manage.py loaddata data.xml
release: python manage.py makemigrations
release: python manage.py migrate

web: python manage.py runserver 0.0.0.0:$PORT
