FROM python:3.9-slim

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENV FLASK_ENV=development
ENV FLASK_APP=/app/xai_app.py
ENV TZ=America/Sao_Paulo

CMD flask run --host=0.0.0.0 --reload
