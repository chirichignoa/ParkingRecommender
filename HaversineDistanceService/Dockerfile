#FROM python:3.6
#
#WORKDIR /app
#
##RUN mkdir -p /server/app/
#
#ENV FLASK_APP app/app.py
#ENV FLASK_ENV dev
#ENV FLASK_DEBUG 1
#
##RUN export FLASK_APP=app/app.py
##RUN export FLASK_ENV=prod
#
## COPY APP
#ADD ./* /app/
## COPY DEPENDENCIES
#ADD ./requirements.txt /app/
#ADD ./config.py /app/
#
#RUN pip install -r /app/requirements.txt
#
#EXPOSE 2525
#CMD ["flask", "run", "--host=0.0.0.0", "--port=2525"]

#FROM python:3.6
#
#ENV FLASK_APP app.py
#ENV FLASK_ENV development
#ENV FLASK_DEBUG 0
#
#WORKDIR /app
#
#
#ADD ./app.py /app/
#
#ADD ./requirements.txt /app/
#
#RUN pip install -U -r requirements.txt
#
#EXPOSE 2525
#
#CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=2525"]
FROM python:3.6
ENV FLASK_ENV development
ENV FLASK_APP app.py
COPY ./* /app/
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 2525
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0", "--port=2525"]
