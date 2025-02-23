FROM python:3.9-slim

WORKDIR /app

COPY rq.txt /app/
RUN  pip install --upgrade pip
RUN pip install --no-cache-dir -r rq.txt

COPY . /app/

EXPOSE 8024
CMD ["python3", "manage.py", "runserver" , "0.0.0.0:8024"]

























