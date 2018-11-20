FROM java:8

WORKDIR /app
ADD /target/MovementsService.jar /app/MovementsService.jar
ENTRYPOINT ["java", "-jar", "MovementsService.jar"]

EXPOSE 4567