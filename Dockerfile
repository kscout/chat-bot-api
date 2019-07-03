FROM python:3.7-slim as base

FROM base as builder

RUN mkdir /install
WORKDIR /install

RUN apt-get clean \
    && apt-get -y update

RUN apt-get -y install nginx \
    && apt-get -y install python3-pip python3-dev \
    && apt-get -y install build-essential

COPY requirements.txt /srv/bot_api/requirements.txt
RUN pip install -r /srv/bot_api/requirements.txt

RUN [ "python", "-c", "import nltk; nltk.download('punkt', download_dir='/srv/bot_api/nltk_data/');nltk.download('stopwords', download_dir='/srv/bot_api/nltk_data/');nltk.download('wordnet', download_dir='/srv/bot_api/nltk_data/')" ]


FROM base

COPY --from=builder /usr /usr
COPY --from=builder /etc /etc
COPY --from=builder /var/lib/nginx /var/lib/nginx
COPY --from=builder /var/log/nginx /var/log/nginx
COPY --from=builder /srv/bot_api/nltk_data/ /srv/bot_api/nltk_data/
COPY . /srv/bot_api

WORKDIR /srv/bot_api
RUN chmod 777 /srv/bot_api

EXPOSE 8080

CMD ["gunicorn", "-b", "0.0.0.0:8080", "app"]