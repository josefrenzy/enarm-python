FROM python:3.10.6-slim-buster
RUN apt-get update
RUN apt-get install software-properties-common -y
RUN pip install --upgrade pip
WORKDIR /app
COPY . /app
RUN ls -la
RUN pip --no-cache-dir install -r requirements.txt
EXPOSE 5001
ENTRYPOINT ["bash","gunicorn.sh"]