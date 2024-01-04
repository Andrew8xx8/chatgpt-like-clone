FROM python:3.10-slim-bookworm

WORKDIR /app

COPY requirements.txt /app/

RUN pip install -r requirements.txt

COPY . /app

EXPOSE 8502

CMD ["streamlit", "run", "app.py"]
