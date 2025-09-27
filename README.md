# RecipeAppAPI-UdemyBusinessCourseDjango
Recipe Django API project - Udemy Business Course

## Building Docker Image
docker build .

## Building docker compose
docker compose run *name_of_the_service*: what this does is to run a temporarily container based on the definition of the service *name_of_the_service*
docker compose up: what this does is to build the whole docker-compose.yml file, so if you define more than one service, you build all of those that are defined on the mentioned file.  

### Project Setup
Makes Docker to execute the Django default command to creating a new app:a
```bash
docker compose run --rm app sh -c "python manage.py startapp core"
```
The previous command creates the template app to our project

### Unit testing
docker-compose run --rm app sh -c "python manage.py test"
* Docker compose run --rm app: tells the terminal to run a temporarily container based on the definition of the service app, and to remove the container after it's done its jobs.
* sh -c: shell command "content inside the quotations is wrote in the shell"
* python manage.py test: Django framework integrated command for running the unit tests.

#### Test Driven Development - Django Test Running
The following command will run the whole test suite
```bash
python manage.py test
```

The following command will run the whole test suite using docker:
```
docker compose run --rm app sh -c "python manage.py test"
```

But if we want to execute a single command/function/test without mocking, we can use:
```
docker compose run --rm app sh -c "python manage.py name_of_the_command"
```

Applied example to this particular project:
```
docker compose run --rm app sh -c "python manage.py wait_for_db
```
The unit testing for this functionality mocks the DB behavior, but if you execute the single command, you get the actual behavior with the real db.

## Flake8 Linting
Comments that tell flake8 to ignore respective file's errors:
```
# noqa
```

To visualize this phenomenon, you can check the app/core/admin.py file, as in first line there is a comment that says # noqa. When executing flake8, the output shouldn't show any linting related to that file.