FROM python:3.10-slim


WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app/

CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]