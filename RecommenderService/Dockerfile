FROM python:3.6

WORKDIR /app

ENV FLASK_APP server.py
ENV FLASK_ENV development
# ENV FLASK_DEBUG 0

RUN export FLASK_APP=server.py
RUN export FLASK_ENV=development

RUN mkdir -p /app/data/
RUN mkdir -p /app/models/
RUN mkdir -p /app/util/

# COPY APP
ADD ./server.py /app/
# COPY DEPENDENCIES
ADD ./requirements.txt /app/
# COPY BINS FOR MODEL
ADD ./data/* /app/data/
# COPY SERIALIZED MODEL
ADD ./models/model.pkl /app/models/
# COPY PREDICTORS FILE
ADD ./util/* /app/util/

RUN pip install -r /app/requirements.txt

EXPOSE 5000 
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
