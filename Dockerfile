FROM python:3.9-bullseye
# RUN apt add build-base

RUN mkdir app
COPY . /app
WORKDIR /app

RUN apt update \
    && apt install -y wkhtmltopdf

RUN pip install -r requirements.txt


EXPOSE 5000
CMD ["python", "application.py"]
