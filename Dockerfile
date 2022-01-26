FROM python:latest
WORKDIR /application
COPY ./requirements.txt /application/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /application/requirements.txt
COPY ./app /application/app
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0"]
