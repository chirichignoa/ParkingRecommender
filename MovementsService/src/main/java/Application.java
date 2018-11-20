import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import service.MovementsService;
import util.Path;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

import static spark.Spark.get;
import static spark.Spark.port;

public class Application {

    private String URL = "";
    private static Logger log = LogManager.getLogger(Application.class);

    public Application(){
        this.init();
    }

    private void init() {
        Properties prop = new Properties();
        InputStream is;
        try {
            is =this.getClass().getClassLoader().getResourceAsStream("properties.properties");
            prop.load(is);
            int port = Integer.parseInt(prop.getProperty("app.port"));
            port(port);
            log.debug("Running at port: " + port);
            get(Path.MOVEMENTS, MovementsService::getMovements);
            get(Path.PARKINGMETER_MOVEMENTS, MovementsService::getAllMovements);
            get(Path.DATERANGE_MOVEMENTS, MovementsService::getAllMovementsByDay);
            get(Path.TIMEINTERVAL_MOVEMENTS, MovementsService::getAllMovementsByInterval);
        } catch(IOException e) {
            System.out.println(e.toString());
        }

    }

    public static void main(String[] args) {
        Application app = new Application();
    }
}