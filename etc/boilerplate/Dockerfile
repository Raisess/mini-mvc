FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.core.txt ./
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r requirements.core.txt

COPY . .

EXPOSE 8080/tcp

CMD ["python", "./src/main.py", "8080", "0.0.0.0"]
