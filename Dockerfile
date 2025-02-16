FROM python:3.12-slim

WORKDIR /ChatReader

COPY requirements.txt requirements.txt
run pip install -r requirements.txt

COPY . .

CMD ["python3", "run.py"]