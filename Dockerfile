# We use alpine because it's extremely lightweight and doesn't contain any unnecessary packages.
# It's the most ideal for Docker containers.
FROM python:3.9-alpine3.13

# Next, we define the maintainer of the image. This means the label of the person who created and maintains the website/docker image.
LABEL maintainer="github.com/03matig"

# Next step is recommended when running Python in Docker containers.
# This tells Python that you don't want to buffer the outputs, as Python bufferes standard output (stdout) and standard error (stderr) by default, which means prints and logs don't appear immediatly,
# until the buffer is flushed (or execution is terminated).
# Python outputs everything directly to the terminal without buffering (delaying) it from reaching the screen, so we can see the logs immediatly as they are running.
ENV PYTHONUNBUFFERED 1

# COPY <origin> <destination_inside_container>, tmp means "temporarily", as in temporarily directory.
COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app

# Next, we set the working directory inside the container to /app.
# The "docker build ." will throw an error if the local ./app/ directory doesn't exist.
WORKDIR /app

# Now, we expose the port that the application will run on, so we can connect to the Django development server.
EXPOSE 8000

# We define a build argument called dev and sets the default argument to false, so in the docker compose when we run it, we overwrite this by specifying the value to args -dev.
ARG DEV=false

# We run a single command on the alpine image to keep the image as lightweight as possible.
# Other thing you could do is to specify this lines individually but in that case, it creates a new image layer for each command we run, but we want to avoid that.
# We create a virtual environment, upgrade pip, install the dependencies from requirements.txt, remove the temporary requirements.txt file and create a new user to run the application not using the
# root user. We also don't create a home directory for the user because we don't need it.

# The virtual environment we create it's because the dependencies we use on our project can conflict with the python version inside the container while they could have no conflicts with the 
# python version of the local machine.
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    fi && \
    rm -rf /tmp && \
    adduser \
        --disabled-password \
        --no-create-home \
        django-user

# Note: if you do an if statement on shell script, to end it you have to write "fi".

# Updates the ENV variable inside the image. The PATH is the environment variable that's automatically created on Linux. It defines all of the directories where executables can be run.
# When we run a command in our project, we don't want to have to specify the full path of our virtual environment.
ENV PATH="/py/bin:$PATH"

# Finally, we switch to the new user we created to run the application, instead of using the root user. 
USER django-user