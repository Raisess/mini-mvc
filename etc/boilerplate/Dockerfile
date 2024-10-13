FROM python:3.12.6-alpine

WORKDIR /usr/src/app

RUN PIP_ROOT_USER_ACTION=ignore pip install wheel

COPY requirements.core.txt ./
RUN pip install --no-cache-dir -r requirements.core.txt

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8080/tcp

CMD ["PRODUCTION=1", "python", "./src/wsgi.py", "8080", "0.0.0.0"]
