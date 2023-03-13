FROM python:3.10.6-slim-buster
ENV CLIENT_ID=623vnb06drds7h0qquvti7o63i
ENV SECRET_HASH=vqclgnm9qri6k3gdmt1328j3drrh63unsq03l3vsirnu0dv01s6
ENV REGION_NAME=us-east-1
RUN apt-get update
RUN apt-get install software-properties-common -y
RUN apt-get -y install default-libmysqlclient-dev
RUN pip install --upgrade pip
WORKDIR /app
COPY . /app
RUN ls -la
RUN pip --no-cache-dir install -r requirements.txt
EXPOSE 5001
ENTRYPOINT ["bash","gunicorn.sh"]