FROM python:3.11
WORKDIR /code
COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
RUN mkdir /app
WORKDIR /app
COPY ./ /app
CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "80"]
