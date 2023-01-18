# https://viblo.asia/p/tao-mot-django-api-trong-vong-20-phut-L4x5xO11lBM
# https://viblo.asia/p/xay-dung-api-voi-django-rest-framework-Do754PXJ5M6
# python3 -m venv ./venv
source venv/bin/activate

# python3 -m pip install --upgrade pip
# pip install django
# pip install djangorestframework
# django-admin startproject proj .
# django-admin startapp dating_app
# pip install django-tastypie
python3 manage.py makemigrations
python3 manage.py migrate

python3 manage.py runserver
