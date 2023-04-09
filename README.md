# pacer-challenge
Pacer take home challenge

## Task 1: Simple Backend Endpoint

### Local Quickstart

1. Navigate to the project directory where `manage.py` is located
2. Create and enter virtual environment `pip -m venv venv`
3. Install package dependencies `pip install -r requirements.txt`
4. Run the development server `py manage.py runserver`
5. Create and run migrations `py manage.py makemigrations && py manage.py migrate`
6. Open endpoint URL `http://<host>/scores/api/get_score/` in browser
7. Enter a number in `input_value` field and try to post it
    ![alt text](/Screenshot%202023-04-09%20165700.png)

### Details
1. A simple Python Django app was developed that has an API endpoint at `/scores/api/get_score/`. The API was created using [Django REST Framework](https://github.com/encode/django-rest-framework). This end point can accessed via `POST` request and does the followings:
    1. Accepts an input parameter `input_value`
    2. Calculates `score` using a custom formula
        - At the moment, the formula is simply `score = input_value + 1`
    3. Records the user and result in the database
        - The fields are `id`, `user`, `score`, and `date_submitted`
        - If the user is not authenticated, the `user` field will be `None`
        - `date_submitted` will be automatically assigned with the current date time

2. Database
    ```python
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        },
        'postgres': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': '<name>',
            'USER': '<user>',
            'PASSWORD': '<password>',
            'HOST': '<host>',
        },
    }
    ```

3. The endpoint was tested using 3 methods:
    1. DRF browsable API
    2. Using httpie
        ```bash
        >> http POST http://127.0.0.1:8000/scores/api/get_score/ input_value=1

        HTTP/1.1 201 Created
        Allow: POST, OPTIONS
        Content-Length: 80
        Content-Type: application/json
        Cross-Origin-Opener-Policy: same-origin
        Date: Sun, 09 Apr 2023 05:31:09 GMT
        Referrer-Policy: same-origin
        Server: WSGIServer/0.2 CPython/3.10.6
        Vary: Cookie
        X-Content-Type-Options: nosniff
        X-Frame-Options: DENY

        {
            "date_submitted": "2023-04-09T05:31:09.058505Z",
            "id": 93,
            "score": 2.0,
            "user": null
        }
        ```
    3. Using Django tests
        ```bash
        >> py manage.py test

        ```

## Task 2: Admin Panel

## Task 3: Database Migration