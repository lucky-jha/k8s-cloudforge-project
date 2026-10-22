#this is multi-stage build
FROM python:3.12-slim-bullseye as build

WORKDIR /app

COPY app/requirements.txt .

RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


# Stage 2 - actual image
FROM python:3.12-slim

RUN groupadd --system app && useradd --system --gid app --no-create-home app

WORKDIR /app

COPY --from=build /install /usr/local

COPY app/app.py .
COPY app/templates ./templates

USER app

ENV PORT=8080 \
    APP_VERSION=dev \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 

EXPOSE 8080

CMD ["python", "app.py"]

