package service;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.json.JSONArray;
import spark.Request;
import spark.Response;
import util.JsonUtil;

import java.sql.SQLException;

public class MovementsService {

    private static Logger log = LogManager.getLogger(MovementsService.class);

    public MovementsService() {

    }

    public static String getMovements(Request request, Response response) throws SQLException {
        String idCuadra = request.queryParams("id_cuadra");
        MovementsDAO dao = MovementsDAO.getInstance();
        JSONArray data;
        if(idCuadra != null)
            data = dao.getMovements(Integer.parseInt(idCuadra));
        else
            data = dao.getMovements(null);
        if(data != null) {
            response.type("application/json");
            response.status(200);
            return data.toString();
        }
        response.status(400);
        return JsonUtil.dataToJson("A problem has occurred");
    }

    public static String getAllMovements(Request request, Response response) throws SQLException {
        String idCuadra = request.queryParams("id_cuadra");
        String dateFrom = request.queryParams("date_from");
        String dateTo = request.queryParams("date_to");
        String hourFrom = request.queryParams("hour_from");
        String hourTo = request.queryParams("hour_to");
        if ((dateFrom == null) || (dateTo == null) || (hourFrom == null) || (hourTo == null)) {
            response.status(400);
            return JsonUtil.dataToJson("The request does not have necessary parameters");
        }
        MovementsDAO dao = MovementsDAO.getInstance();
        JSONArray data;
        if(idCuadra != null)
            data = dao.getAllMovements(Integer.parseInt(idCuadra), dateFrom, dateTo, hourFrom, hourTo);
        else
            data = dao.getAllMovements(null, dateFrom, dateTo, hourFrom, hourTo);
        if(data != null) {
            response.type("application/json");
            response.status(200);
            return data.toString();
        }
        response.status(400);
        return JsonUtil.dataToJson("A problem has occurred");
    }

    public static String getAllMovementsByDay(Request request, Response response) throws SQLException {
        String idCuadra = request.queryParams("id_cuadra");
        String dateFrom = request.queryParams("date_from");
        String hourFrom = request.queryParams("hour_from");
        String hourTo = request.queryParams("hour_to");
        if ((dateFrom == null) || (hourFrom == null) || (hourTo == null)) {
            response.status(400);
            return JsonUtil.dataToJson("The request does not have necessary parameters");
        }
        log.debug("Getting all movements for parkingmeter: " + idCuadra);
        MovementsDAO dao = MovementsDAO.getInstance();
        JSONArray data;
        if(idCuadra != null)
            data = dao.getAllMovementsByDay(Integer.parseInt(idCuadra), dateFrom, hourFrom, hourTo);
        else
            data = dao.getAllMovementsByDay(null, dateFrom, hourFrom, hourTo);
        if(data != null) {
            response.type("application/json");
            response.status(200);
            return data.toString();
        }
        response.status(400);
        return JsonUtil.dataToJson("A problem has occurred");
    }

    public static String getAllMovementsByInterval(Request request, Response response) throws SQLException {
        String idCuadra = request.queryParams("id_cuadra");
        String dateFrom = request.queryParams("date_from");
        String hourFrom = request.queryParams("hour_from");
        int nIdCuadra;
        if ((dateFrom == null) || (hourFrom == null)) {
            response.status(400);
            return JsonUtil.dataToJson("The request does not have necessary parameters");
        }
        log.debug("Getting all movements for parkingmeter: " + idCuadra);
        MovementsDAO dao = MovementsDAO.getInstance();
        JSONArray data;
        if(idCuadra != null)
            data = dao.getAllMovementsByInterval(Integer.parseInt(idCuadra), dateFrom, hourFrom);
        else
            data = dao.getAllMovementsByInterval(null, dateFrom, hourFrom);
        if(data != null) {
            response.type("application/json");
            response.status(200);
            return data.toString();
        }
        response.status(400);
        return JsonUtil.dataToJson("A problem has occurred");
    }

}
