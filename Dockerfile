FROM python:3.6
RUN mkdir -p /app/user
RUN mkdir -p /src
WORKDIR /app/user
ADD src/requirements.txt /app/user/
RUN pip install --src /src -r requirements.txt
