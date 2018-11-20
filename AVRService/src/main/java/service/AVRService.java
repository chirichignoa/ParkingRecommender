package service;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.json.JSONArray;
import spark.Request;
import spark.Response;
import util.JsonUtil;

import java.sql.SQLException;

public class AVRService {

    private static Logger log = LogManager.getLogger(AVRService.class);

    public AVRService() {

    }

    public static String getAvr(Request request, Response response) throws SQLException {
        String idCuadra = request.queryParams("id_cuadra");
        String date = request.queryParams("date");
        String hour = request.queryParams("hour");
        if ((date == null) || (hour == null)) {
            response.status(400);
            return JsonUtil.dataToJson("The request does not have necessary parameters");
        }
        AvrDAO dao = AvrDAO.getInstance();
        JSONArray data;
        if(idCuadra != null)
            data = dao.getAvr(Integer.parseInt(idCuadra), date, hour);
        else
            data = dao.getAvr(null, date, hour);
        if(data != null) {
            response.type("application/json");
            response.status(200);
            return data.toString();
        }
        response.status(400);
        return JsonUtil.dataToJson("A problem has occurred");
    }

}
