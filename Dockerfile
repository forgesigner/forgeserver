FROM python:3.9-slim

WORKDIR /
COPY . .

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "server.py"]
