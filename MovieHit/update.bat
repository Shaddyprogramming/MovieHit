   @echo off
   REM Activate the virtual environment
   call env\Scripts\activate

   REM Run your command here
   python manage.py collectstatic --noinput

   REM Close the command prompt automatically
   exit
   