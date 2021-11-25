FROM python:3.8
COPY . /app
WORKDIR /app
RUN apt update \
    && apt install -y wkhtmltopdf

RUN pip install -r requirements.txt
EXPOSE 5000

CMD ["python", "application.py"]
