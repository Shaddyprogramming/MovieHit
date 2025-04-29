@echo off
REM Activate the virtual environment
call env\Scripts\activate

REM Collect static files
python manage.py collectstatic --noinput

REM Close the command prompt automatically
exit
   