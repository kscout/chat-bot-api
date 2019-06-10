FROM python:3.7-slim

COPY . /srv/bot_api
WORKDIR /srv/bot_api

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install python3-pip python3-dev \
    && apt-get -y install build-essential

RUN pip3 install -r requirements.txt

RUN [ "python", "-c", "import nltk; nltk.download('punkt', download_dir='/srv/bot_api/nltk_data/');nltk.download('stopwords', download_dir='/srv/bot_api/nltk_data/');nltk.download('wordnet', download_dir='/srv/bot_api/nltk_data/')" ]

COPY deploy/nginx.conf /etc/nginx
RUN chmod +x ./nginxstart.sh
CMD ["./nginxstart.sh"]