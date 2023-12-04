FROM python:3.8-slim

WORKDIR /server
COPY . .

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "--port=5000", "server:server"]
