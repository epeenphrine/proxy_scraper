FROM python:3.7

WORKDIR /proxies/

COPY . .

RUN apt-get update -y && pip install pipenv && pipenv install -r requirements.txt

CMD pipenv run python -c 'import proxyscrape; proxyscrape.proxyscrape()'