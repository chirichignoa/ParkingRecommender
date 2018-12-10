FROM java:8

WORKDIR /app
COPY /target/MovementsService.jar /app
ENTRYPOINT ["java", "-jar", "MovementsService.jar"]

EXPOSE 4567