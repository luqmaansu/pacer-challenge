# pacer-challenge
Pacer take home challenge

### Test
Using httpie
```bash
>> http POST http://127.0.0.1:8000/scores/api/get_score/ input_value=1
```
Response:
```
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
Using Django tests
```bash
py manage.py test
```
