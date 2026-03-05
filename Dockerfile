FROM python:3.10

WORKDIR /app

RUN apt-get update && apt-get install -y \
    jq \
    curl \
    dos2unix

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN dos2unix generate-keys.sh test-auth-flow.sh
RUN chmod +x generate-keys.sh test-auth-flow.sh

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]