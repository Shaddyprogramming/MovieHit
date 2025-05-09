@echo off
REM Activate the virtual environment (if applicable)
REM Replace "env\Scripts\activate" with the path to your virtual environment
call env\Scripts\activate

REM Run the Django shell and execute the backfill script
python manage.py shell -c "import uuid; from MovieHit.management.movies import Movies; [setattr(movie, 'unique_id', uuid.uuid4()) or movie.save() for movie in Movies.objects.filter(unique_id__isnull=True)]; print('Backfill complete!')"

REM Deactivate the virtual environment (if applicable)
deactivate
