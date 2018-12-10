FROM java:8

WORKDIR /app
COPY /target/ParkingMetersService.jar /app
ENTRYPOINT ["java", "-jar", "ParkingMetersService.jar"]

EXPOSE 4567
