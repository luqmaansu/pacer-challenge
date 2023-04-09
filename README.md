# pacer-challenge
Pacer take home challenge

## Task 1: Simple Backend Endpoint

1. A simple Python Django app was developed that has an API endpoint at `/scores/api/get_score/`. This end point can accessed via `POST` request and does the followings:
    1. Accepts an input parameter `input_value`
    2. Calculates `score` using a custom formula
        - At the moment, the formula is simply `score = input_value + 1`
    3. Records the user and result in the database
        - The fields are `id`, `user`, `score`, and `date_submitted`
        - If the user is not authenticated, the `user` field will be `None`
        - `date_submitted` will be automatically assigned with the current date time

2. The endpoint was tested using 3 methods:
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
