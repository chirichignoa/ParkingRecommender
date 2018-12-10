FROM java:8

WORKDIR /app
COPY /target/AVRService.jar /app
ENTRYPOINT ["java", "-jar", "AVRService.jar"]

EXPOSE 4569