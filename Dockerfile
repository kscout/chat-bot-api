FROM python:3.7-slim

COPY . /srv/bot_api
WORKDIR /srv/bot_api

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install python3-pip python3-dev \
    && apt-get -y install build-essential

RUN pip3 install -r requirements.txt

RUN rm /etc/nginx/sites-enabled/default
RUN rm -r /root/.cache

RUN [ "python", "-c", "import nltk; nltk.download('punkt', download_dir='/srv/bot_api/nltk_data/');nltk.download('stopwords', download_dir='/srv/bot_api/nltk_data/');nltk.download('wordnet', download_dir='/srv/bot_api/nltk_data/')" ]

RUN chmod -R 777 /var/log/nginx /var/run /var/lib/nginx \
     && chgrp -R 0 /etc/nginx \
     && chmod -R g+rwX /etc/nginx

RUN rm -v /etc/nginx/nginx.conf
COPY deploy/nginx.conf /etc/nginx

RUN chmod 777 ./nginxstart.sh

CMD ["nginx", "-g", "daemon off;"]

EXPOSE 8080

CMD ["./nginxstart.sh"]