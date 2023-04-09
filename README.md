# pacer-challenge
Pacer take home challenge

## Task 1: Simple Backend Endpoint

### Live API endpoint
If you want to test this live in the cloud;

1. [luqmaansu.pythonanywhere.com/scores/api/get_score/](https://luqmaansu.pythonanywhere.com/scores/api/get_score/)
2. Quick test with httpie
    ```cmd
    http POST http://luqmaansu.pythonanywhere.com/scores/api/get_score/ input_value=1 user=1
    ```

### Local Quickstart
If you want to try to run this locally;
1. Navigate to the project directory where `manage.py` is located
2. Create and enter virtual environment `pip -m venv venv`
3. Install package dependencies `pip install -r requirements.txt`
4. Create an `.env` file with sample values:
    ```
    DEBUG=True
    SECRET_KEY=q!W-5"I5QErgfe_kD[CjPY1=^zg>4+:?~=88SXowVu>kgdap3l^ukVO..]
    ```
5. Run the development server `py manage.py runserver`
6. Create and run migrations `py manage.py makemigrations && py manage.py migrate`
7. Open endpoint URL `http://<host>/scores/api/get_score/` in browser
8. Enter a number in `input_value` field, optionally select a `user`, and try to post it

### API endpoint
1. A simple Python Django app was developed that has an API endpoint at `/scores/api/get_score/`. The API was created using [Django REST Framework](https://github.com/encode/django-rest-framework). This endpoint can accessed via `POST` request and does the followings:
    1. Accepts input parameters `input_value` and `user` (id number)
    2. Calculates `score` using a custom formula
        - At the moment, the formula is simply `score = input_value + 1`
    3. Records the user and result in the database
        - The fields are `id`, `user`, `score`, and `date_submitted`
        - If the `user` id does not correspond to an existing user, an error will be returned
        - `date_submitted` will be automatically assigned with the current date time

### Database
The default database uses SQLite in development (signalled by when `DEBUG == True`), and uses a live PostgreSQL in the cloud in production (when `DEBUG == False`). Note that the database details are hidden in an environment variable using [django-environ](https://github.com/joke2k/django-environ) package.

```python
if DEBUG == True:
    # Development database
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        },
    }
else:
    # Production database
    DATABASES = {
        'default': env.db()
    }
```

### Testing
The endpoint was tested using 3 methods:
1. DRF browsable API
    ![alt text](/readme/images/Screenshot%202023-04-09%20165700.png)
2. Using [HTTPie](https://github.com/httpie/httpie)
    ```cmd
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

    A few test cases were created in `scores/tests.py` to test various aspects of the endpoint.
    ```cmd
    >> py manage.py test
    Found 7 test(s).
    Creating test database for alias 'default'...
    System check identified no issues (0 silenced).
    .......
    ----------------------------------------------------------------------
    Ran 7 tests in 0.058s

    OK
    Destroying test database for alias 'default'...
    ```

## Task 2: Admin Panel

An Admin panel was created that enables the user to see the list of scores. To access this page, following these steps:

1. Create a superuser
    ```bash
    >> py manage.py createsuperuser
    # Follow the prompts and enter credentials
    ```
2. Go to `/admin/` in the URL and log in

    Depending on the permission granted, permitted staff users can also access the Users database, and some can also be granted permission either to view, create, edit, delete, or any combination of those operations on any table (e.g., Users, or Scores). ![alt text](/readme/images/Screenshot%202023-04-09%20210017.png)

    There's a tonne of further customizations that can be done here, but as per task instruction, suffice to create a simple admin panel with some basic customizations. Note that there is a custom filter function at the right sidebar.

## Task 3: Database Migration

Process summary:
1. Ensure model tests are set up and passed
1. Consider backing up both producation and development database
1. Make changes in the relevant `models.py` files
1. Make migration files `py manage.py makemigrations`
1. Inspect the migration files and modify if needed
1. Run migrations `py manage.py migrate`
1. Run tests
1. Run migrations in production, run tests, and monitor usage

### 1. Ensure model tests are set up and passed
This will help to ensure that the intended behaviour of the model, through relationships, methods, and properties, are not affected by the changes.

### 2. Consider backing up both producation and development database
If the changes involve potentially risky changes (especially removing or renaming columns), backup the database. One of the simplest ways to do this for simple data is via Django's `dumpdata` command.
```bash
# create backup file
>> py manage.py dumpdata datadump.json

# load backup file into current database
>> py manage.py loaddata datadump.json
```

A more advanced and proper alternative would be to use a third-party package like [django-dbbackup](https://github.com/jazzband/django-dbbackup).

### 3. Analyze the effects of the proposed change
Adding fields usually do not have much dangerous effects. Deleting and editing, on the other, potentially do have risky effects, such as those that affect other relationships, methods, and properties. While these things can be tested with good testing programs, if they fail *after* doing destructive changes, the original state and/or current data may possibly be unlikely to be recovered easily.

One quick way to check this is by searching through the whole code base (e.g., using VS Code, with `Ctrl + Shift + F`) and search through all places that refer to the fields and/or models being proposed to be changed.

### 4. Make changes in the relevant `models.py` files
This is where the essence of the table schema is defined, in which Django will use to create the SQL tables. This may involve adding, editing, or removing model fields.

### 5. Make migration files `py manage.py makemigrations`
During this step, Django will help to do various checkings such as ensuring no name clashing, imports are correct, and others, and then create a "migration file" that contains a list of proposed operations to the database. If there are any error that arise when running this command, identify the issue and solve it.

If the modification of `models.py` involves renaming fields, very importantly, be aware of whether the `makemigrations` command detect this as renaming fields, and not removing fields. If a renamed field is considered removed, and if there is previous data in that field, proceeding further can make present data permanently lost.

### 6. Inspect the migration files and modify if needed
Further to the important cognizance above, open the migration files that have just been created and inspect the proposed modifications. In some cases, if the intended change was just to rename a field, but the migrations detect this as deleting an old field and replacing it with a new one. In that case, the migration file needs to be manually changed.

### 7. Run migrations `py manage.py migrate`
Execute the proposed changes on the database. If there are any errors, troubleshoot and solve. Sometimes this might involve rolling back to a previous migration, but take note that in some cases, if it has involved deleting some data, those might need to be recovered via the backup files.

### 8. Run tests and monitor use
Usually the second most nervous part, run the tests to ensure all other behaviours are still working as expected.

### 9. Run migrations in production and monitor usage
Usually the most nervous part, execute the changes and monitor usage in the actual production environment.


## Bonus Task: Deployment to cloud

The application is deployed on [PythonAnywhere](https://www.pythonanywhere.com/user/luqmaansu/), a Platform-as-a-Service application by Anaconda, with PostgreSQL database hosted on [ElephantSQL](https://www.elephantsql.com/).
- API endpoint [luqmaansu.pythonanywhere.com/scores/api/get_score/](https://luqmaansu.pythonanywhere.com/scores/api/get_score/)
- Admin panel [luqmaansu.pythonanywhere.com/admin](https://luqmaansu.pythonanywhere.com/admin/)

---
End