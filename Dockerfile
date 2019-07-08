FROM python:3.7-alpine as base

FROM base as builder

RUN mkdir /install
WORKDIR /install

RUN apk update

RUN apk add libffi-dev openssl-dev gcc build-base

COPY Requirements/requirements.txt /requirements.txt
RUN pip3 install -r /requirements.txt

RUN apk add --virtual scipy-build
RUN pip3 install --upgrade setuptools

#RUN echo "http://dl-8.alpinelinux.org/alpine/edge/community" >> /etc/apk/repositories
#RUN ln -s /usr/include/locale.h /usr/include/xlocale.h
COPY Requirements/requirements-nlp.txt /requirements-nlp.txt
RUN pip3 install --no-cache-dir -r /requirements-nlp.txt

RUN mkdir -p /srv/bot_api/nltk_data

RUN [ "python", "-c", "import nltk; nltk.download('punkt', download_dir='/srv/bot_api/nltk_data/'); \
       nltk.download('stopwords', download_dir='/srv/bot_api/nltk_data/'); \
       nltk.download('wordnet', download_dir='/srv/bot_api/nltk_data/')" ]

FROM base

COPY --from=builder /usr /usr
COPY --from=builder /srv/bot_api/nltk_data/ /srv/bot_api/nltk_data/
COPY . /srv/bot_api

WORKDIR /srv/bot_api
RUN chmod 777 /srv/bot_api
RUN chmod 777 gunicornstart.sh

EXPOSE 8080

CMD ["./gunicornstart.sh"]