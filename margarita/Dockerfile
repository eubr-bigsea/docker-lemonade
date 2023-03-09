FROM python:3.10.9-alpine3.17

RUN apk add --no-cache bash curl vim doas

RUN adduser peel -G wheel; \
    echo '123456' | chpasswd; \
    echo 'permit :wheel as root' > /etc/doas.d/doas.conf
USER peel

ENV FLASK_APP margarita.py

ENV PATH ${PATH}:/home/peel/.local/bin

WORKDIR /home/peel

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY gunicorn_config.py boot.sh margarita.py request_lemonade.py ./

EXPOSE 5000
ENTRYPOINT ["./boot.sh"]



