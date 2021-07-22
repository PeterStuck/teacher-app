
@echo off

ECHO SEARCHING FOR APP FILES
D:
cd Projekty/Python/wku_django
ECHO COLLECTED

ECHO ACTIVATING VIRTUAL ENVIROMENT
call .\venv\Scripts\activate

ECHO STARTING THE APP
python manage.py runserver 8005

pause