import parkingmeters_service.ParkingMetersService;
import util.Path;

import static spark.Spark.get;
import static spark.Spark.port;

public class Application {

    public Application(){
        this.init();
    }

    private void init() {
        port(4567);
        get(Path.PARKING_METERS, ParkingMetersService::getAllParkingMeters);
    }

    public static void main(String[] args) {
        Application app = new Application();
    }
}
