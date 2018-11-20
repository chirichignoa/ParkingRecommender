FROM python:3.6

WORKDIR /app

RUN mkdir -p /app/server

ENV FLASK_APP server/app.py
ENV FLASK_ENV prod
# ENV FLASK_DEBUG 0

# COPY APP
ADD app/* /app/server
ADD config.py /app
# COPY DEPENDENCIES
ADD ./requirements.txt /app/

RUN pip install -r /app/requirements.txt

EXPOSE 2525
CMD ["flask", "run", "--host=0.0.0.0", "--port=2525"]
