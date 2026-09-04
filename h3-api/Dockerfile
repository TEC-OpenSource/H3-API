FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

COPY requirements.txt .

RUN pip install \
    --no-cache-dir \
    --only-binary=:all: \
    -r requirements.txt

COPY app ./app

RUN useradd \
    --create-home \
    --shell /usr/sbin/nologin \
    appuser

USER appuser

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
