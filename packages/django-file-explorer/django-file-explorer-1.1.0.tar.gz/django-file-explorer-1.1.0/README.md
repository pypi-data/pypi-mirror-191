# Django File Explorer

A django app to explore the host machine directory. 

It will provide following features:

1. Allow user login
2. Allow to set roles for user to delete and download directories.
3. Allow user to upload single file.

## Installation

Following command will help to install the package.

```bash
pip install django-file-explorer
```

## Setup

1. Add the app to **setting.py** file in **INSTALLED_APPS** section.

```python
INSTALLED_APPS = [
    ...
    'explorer.apps.ExplorerConfig',
]
```

2. Make the migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

3. Add URL to **urls.py** file.

```python
from django.urls import include

urlpatterns = [
    ...
    path('explorer/', include('explorer.urls'), name='explorer')
]
```

4. Add following **actions** to database
   1. download
   2. delete
   3. upload

Add **volumes** to database by specifying its name and path. After that define the user roles for specific volume in **user roles** table.

## Run

Go to explorer url **SERVER:PORT/explorer** and explore the volumes.

## Author

**Tahir Rafique**
