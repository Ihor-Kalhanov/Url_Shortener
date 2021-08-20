FROM python:3.7
ENV PYTHONUNBUFFERED=1
COPY requirements.txt /
RUN apt-get update && apt-get update -y && pip install --no-cache-dir -r requirements.txt
COPY . /web
WORKDIR /web
EXPOSE 5001
CMD [ "python", "web/app.py" ]