FROM python:3.6
ENV PYTHONUNBUFFERED 1

# Install Dockerize
RUN apt-get update && apt-get install -y wget
ENV DOCKERIZE_VERSION v0.6.1
RUN wget https://github.com/jwilder/dockerize/releases/download/$DOCKERIZE_VERSION/dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && tar -C /usr/local/bin -xzvf dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz \
    && rm dockerize-linux-amd64-$DOCKERIZE_VERSION.tar.gz

# Copy current dir (AIhome) into container /code
RUN mkdir /code
WORKDIR /code
COPY . /code/
RUN python3 -m pip install -r requirements.txt
CMD dockerize python ./wsgi.py
