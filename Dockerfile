FROM python:3.12-slim

WORKDIR /ChatReader

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH="/ChatReader"


CMD ["python3", "run.py"]