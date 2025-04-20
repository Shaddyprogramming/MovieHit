@echo off
REM Run migrations
python manage.py makemigrations
python manage.py migrate

REM Write genres to a file
exit
