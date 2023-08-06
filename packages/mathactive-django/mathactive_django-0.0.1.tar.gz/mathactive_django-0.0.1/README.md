# MathActive

MathActive is a Django app to manage your conversational activities for students learning math.

Detailed documentation is in the `docs/` directory.

## Quick start

### 1. Add "mathactive" to your INSTALLED_APPS

Your django project's `settings.py` should look like this:

#### *`your_django_project/settings.py`*
```python
INSTALLED_APPS = [
    ...
    'mathactive',
]
```

### 2. Include the mathactive URLs (routes) in your project `urls.py` like this:

#### *`your_django_project/urls.py`*
```python
path('mathactive/', include('mathactive.urls')),
```

### 3. Run `python manage.py migrate`

The `migrate` command will create the mathactive database tables using the Django data models defined in `mathactive/models.py`.

### 4. Run `python manage.py runserver`

The `runserver` command starts the development server.
You can visit [127.0.0.1:8000/admin](http://127.0.0.1:8000/admin/) in your browser (`firefox http://127.0.0.1/admin`) to create a math activity (conversation) for your students.

### 5. Test your mathactive conversation

You can visit [127.0.0.1:8000/mathactive](http://127.0.0.1:8000/mathactive/) to test your mathactive conversation or activity.
