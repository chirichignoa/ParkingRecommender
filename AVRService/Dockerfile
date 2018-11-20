FROM java:8

WORKDIR /app
ADD /target/AVRService.jar /app/AVRService.jar
ENTRYPOINT ["java", "-jar", "AVRService.jar"]

EXPOSE 4569