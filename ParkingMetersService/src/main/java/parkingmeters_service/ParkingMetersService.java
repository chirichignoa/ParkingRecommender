package parkingmeters_service;

import com.google.gson.JsonObject;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.json.JSONArray;
import org.json.JSONObject;
import spark.Request;
import spark.Response;
import util.JsonUtil;


import java.sql.*;
import java.util.List;

public class ParkingMetersService {

    private static Logger log = LogManager.getLogger(ParkingMetersService.class);

    public ParkingMetersService() {

    }

    public static String getAllParkingMeters(Request request, Response response) throws SQLException {
        log.debug("Getting all parkingmeters");
        ParkingMetersDAO dao = ParkingMetersDAO.getInstance();
        JSONArray data = dao.getAllParkingMeters();
        if(data != null) {
            response.type("application/json");
            response.status(200);
//            return JsonUtil.dataToJson(data);
            return data.toString();
        }
        response.status(200);
        return JsonUtil.dataToJson("A problem has occurred");
    }

}
