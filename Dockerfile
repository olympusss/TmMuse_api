FROM python:3.7.0

COPY ./ /app
COPY ./requirements.txt /app

WORKDIR /app

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--reload"]