FROM java:8

WORKDIR /app
ADD /target/ParkingMetersService.jar /app/ParkingMetersService.jar
ENTRYPOINT ["java", "-jar", "ParkingMetersService.jar"]

EXPOSE 4567
