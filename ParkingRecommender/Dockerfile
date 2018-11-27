FROM python:3.6

WORKDIR /app

#RUN mkdir -p /app/app/

ENV FLASK_APP app.py
ENV FLASK_ENV prod
# ENV FLASK_DEBUG 0

RUN export FLASK_APP=app.py
RUN export FLASK_ENV=prod

## COPY APP
#ADD ./app/* /server/
## COPY DEPENDENCIES
#ADD ./requirements.txt /server/
#
#ADD ./config.py /server/
ADD ./* /app/

RUN pip install -r /app/requirements.txt

EXPOSE 4000
CMD ["flask", "run", "--host=0.0.0.0", "--port=4000"]
