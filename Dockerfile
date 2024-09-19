FROM python:3.11.2-slim-buster  

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt


RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]
