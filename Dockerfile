# Build backend
FROM python:3.10-bullseye as build-backend
WORKDIR /app
COPY requirements.txt ./
RUN apt-get update && apt-get install -y gcc
RUN pip install --upgrade pip && pip install -r requirements.txt
COPY . .

# Expose and run the FastAPI server
EXPOSE 14374
RUN chmod +x /app/launch.sh
ENTRYPOINT ["sh", "-c", "./launch.sh"]