Description
Kanvas's API with criation, list and authentication of users (facilitador, instrutor and estudante), criation of courses and update of course's students, criation and grade upgrade of activities.

Dev
Luiz Almeida - All

Tecnologias
Black, Django, and Django Rest Framework

Instalação
Use command python -m venv .venv to create a venv.
Use command source .venv/bin/activate to active de venv.
Use command pip install -r requirements.txt to install all tecnologies.
Use command ./manage.py makemigrations to configurate the tables.
Use command ./manage.py migrate to create the tables.
Use command ./manage.py runserver to start the server localy.

Rotas

ROOT - "/api/".
"/accounts" ["POST"] - To creater a user.

Estudante - terá ambos os campos is_staff e is_superuser com o valor False
Facilitador - terá os campos is_staff == True e is_superuser == False
Instrutor - terá ambos os campos is_staff e is_superuser com o valor True

Estudante:

```
    Body request:
    {
        "username": "student",
        "password": "1234",
        "is_superuser": false,
        "is_staff": false
    }

    Status: 201_CREATED
    Response:
    {
        "id": 1,
        "username": "student",
        "is_superuser": false,
        "is_staff": false
    }
```

Facilitador:

```
    Body request:
        {
            "username": "student",
            "password": "1234",
            "is_superuser": false,
            "is_staff": true
        }

        Status: 201_CREATED
        Response:
        {
            "id": 1,
            "username": "student",
            "is_superuser": false,
            "is_staff": true
        }
```

Instrutor:

```
    Body request:
        {
            "username": "student",
            "password": "1234",
            "is_superuser": true,
            "is_staff": true
        }

        Status: 201_CREATED
        Response:
        {
            "id": 1,
            "username": "student",
            "is_superuser": true,
            "is_staff": true
        }
```

"/login" ["POST"] - To Authenticate user.

```
    Body Request:
        {
            "username": "student",
            "password": "1234"
        }

    Status: 200_OK
    Response:
        {
            "token": "dfd384673e9127213de6116ca33257ce4aa203cf"
        }
```

"/courses" ["POST"] - To create a course, must be logged as Instrutor.

```
    Header -> Authorization: Token <instrutor-token>
    Body Request:
        {
            "name": "Javascript 101"
        }

    Status: 201_CREATED
    Response:
        {
            "id": 1,
            "name": "Javascript 101",
            "user_set": []
        }
```

"/courses/registrations" ["PUT"] - To update course's students list, must be logged as Instrutor.

```
    Header -> Authorization: Token <instrutor-token>
    Body Request:
        {
            "course_id": 1,
            "user_ids": [1, 2, 7]
        }

    Status: 201_CREATED
    Response:
    {
        "id": 1,
        "name": "Javascript 101",
        "user_set": [
            {
                "id": 1,
                "is_superuser": false,
                "is_staff": false,
                "username": "luiz"
            },
            {
                "id": 7,
                "is_superuser": false,
                "is_staff": false,
                "username": "isabela"
            },
            {
                "id": 2,
                "is_superuser": false,
                "is_staff": false,
                "username": "raphael"
            }
        ]
    }
```

Can remove a lot students when you update the course.

```
    Header -> Authorization: Token <facilitador-token or instrutor-token>
    Body Request:
        {
            "course_id": 1,
            "user_ids": [1]
        }

    Status: 201_CREATED
    Response:
    {
        "id": 1,
        "name": "Javascript 101",
        "user_set": [
            {
                "id": 1,
                "is_superuser": false,
                "is_staff": false,
                "username": "luiz"
            },
        ]
    }
```

"/courses" ["GET"] - To get all course.

```
    Status: 200_OK
    Response:
    [
        {
            "id": 1,
            "name": "Javascript 101",
            "user_set": [
                {
                    "id": 1,
                    "is_superuser": false,
                    "is_staff": false,
                    "username": "luiz"
                }
            ]
        },
        {
            "id": 2,
            "name": "Python 101",
            "user_set": []
        }
    ]
```

"/api/activities" ["POST"] - Create an activity, must be logged as Estudante and just can just create the activity and the grade will be null.

```
    Header -> Authorization: Token <estudante-token>
    Body Request:
        {
            "repo": "gitlab.com/cantina-kenzie",
            "grade": 10 // This field id optional
        }

    Status: 201_CREATED
    Response:
    {
        "id": 1,
        "user_id": 1,
        "repo": "gitlab.com/cantina-kenzie",
        "grade": null
    }
```

"/api/activities" ["PUT"] - Update an activity, must be logged as Instrutor or Facilitador to update the activity's grade.

```
    Header -> Authorization: Token <facilitador-token or instrutor-token>
    Body Request:
        {
            "id": 1,
            "grade": 10
        }

    Status: 201_CREATED
    Response:
    {
        "id": 1,
        "user_id": 1,
        "repo": "gitlab.com/cantina-kenzie",
        "grade": 10
    }
```

"/api/activities" ["GET"] - To get all activities, if is logged as Estudante will show just the Estudante's activities, if logged as Facilitador or Intructor will show all activities.

Logged as Estudante:

```
    Header -> Authorization: Token <estudante-token>
    Status: 200_OK
    Response:
    [
        {
            "id": 1,
            "user_id": 1,
            "repo": "github.com/luiz/cantina",
            "grade": null
        },
        {
            "id": 6,
            "user_id": 1,
            "repo": "github.com/hanoi",
            "grade": null
        },
        {
            "id": 15,
            "user_id": 1,
            "repo": "github.com/foodlabs",
            "grade": null
        },
    ]
```

Logged as Facilitador or Instrutor:

```
    Header -> Authorization: Token <facilitador-token or instrutor-token>
    Status: 200_OK
    Response:
    [
        {
            "id": 1,
            "user_id": 1,
            "repo": "github.com/luiz/cantina",
            "grade": null
        },
        {
            "id": 6,
            "user_id": 1,
            "repo": "github.com/hanoi",
            "grade": null
        },
        {
            "id": 10,
            "user_id": 2,
            "repo": "github.com/foodlabs",
            "grade": null
        },
        {
            "id": 35,
            "user_id": 3,
            "repo": "github.com/kanvas",
            "grade": null
        },
    ]
```

"/api/activities/<int:user_id>" ["GET"] - To filter Estudante's activities when logged as Intrutor or Facilitador.

```
    Header -> Authorization: Token <facilitador-token or instrutor-token>
    Status: 200_OK
    Response:
    [
        {
            "id": 1,
            "user_id": 1,
            "repo": "github.com/luiz/cantina",
            "grade": null
        },
        {
            "id": 6,
            "user_id": 1,
            "repo": "github.com/hanoi",
            "grade": null
        },
        {
            "id": 15,
            "user_id": 1,
            "repo": "github.com/foodlabs",
            "grade": null
        },
    ]
```
