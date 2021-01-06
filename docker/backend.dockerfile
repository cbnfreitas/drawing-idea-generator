FROM python:3.8-slim

RUN apt-get update && apt-get install -y libpq-dev gcc

COPY Pipfile* ./
RUN pip install pipenv
RUN pipenv install --system --deploy

RUN apt-get autoremove -y gcc

COPY ./app /app

ARG DEV_MODE=0
EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", 2]