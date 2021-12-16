FROM python:3.7.0

COPY ./requirements.txt /

WORKDIR /

RUN pip install -r requirements.txt

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host=0.0.0.0", "--reload"]