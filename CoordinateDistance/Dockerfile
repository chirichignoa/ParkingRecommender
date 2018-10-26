FROM python:3.6

WORKDIR /app

ENV FLASK_APP app.py
ENV FLASK_ENV development
# ENV FLASK_DEBUG 0

# COPY APP
ADD ./app.py /app/
# COPY DEPENDENCIES
ADD ./requirements.txt /app/

RUN pip install -r /app/requirements.txt

EXPOSE 2525
CMD ["flask", "run", "--host=0.0.0.0", "--port=2525"]
