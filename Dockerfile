FROM python:3.7
COPY requirements.txt /
RUN pip install -r /requirements.txt
COPY . /web
WORKDIR /web
EXPOSE 5001
CMD [ "python", "app.py" ]