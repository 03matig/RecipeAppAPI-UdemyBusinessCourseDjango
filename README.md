# RecipeAppAPI-UdemyBusinessCourseDjango
Recipe Django API project - Udemy Business Course

## Building Docker Image
docker build .

## Building docker compose
docker compose run *name_of_the_service*: what this does is to run a temporarily container based on the definition of the service *name_of_the_service*
docker compose up: what this does is to build the whole docker-compose.yml file, so if you define more than one service, you build all of those that are defined on the mentioned file.  

### Unit testing
docker-compose run --rm app sh -c "python manage.py test"
* Docker compose run --rm app: tells the terminal to run a temporarily container based on the definition of the service app, and to remove the container after it's done its jobs.
* sh -c: shell command "content inside the quotations is wrote in the shell"
* python manage.py test: Django framework integrated command for running the unit tests.

#### Django Test Running
The following command will run the whole test suite
```bash
python manage.py test
```
