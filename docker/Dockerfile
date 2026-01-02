FROM python:3.10-slim
RUN adduser my-app-user --disabled-password

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

WORKDIR /api
COPY apps/ .
COPY core/ .
COPY manage.py .
USER my-app-user
EXPOSE 8000
