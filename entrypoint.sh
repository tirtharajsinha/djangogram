python3 manage.py makemigrations
python3 manage.py migrate
python manage.py collectstatic --no-input
daphne -b 0.0.0.0 -p 8000 core.asgi:application