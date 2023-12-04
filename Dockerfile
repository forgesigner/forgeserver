FROM python:3.9-slim

WORKDIR /server
COPY . .

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

CMD ["python", "server.py", "--port", "4000"]
