FROM python:3.11-slim
WORKDIR /app
COPY . /app
EXPOSE 8080
ENTRYPOINT ["python", "app_ia_production.py"]