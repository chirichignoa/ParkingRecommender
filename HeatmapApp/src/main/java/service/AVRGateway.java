package service;

import com.mashape.unirest.http.HttpResponse;
import com.mashape.unirest.http.JsonNode;
import com.mashape.unirest.http.Unirest;
import com.mashape.unirest.http.exceptions.UnirestException;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import spark.Request;
import spark.Response;
import util.JsonUtil;

import java.io.IOException;
import java.io.InputStream;
import java.util.Properties;

public class AVRGateway {

    private static Logger log = LogManager.getLogger(AVRGateway.class);
    private static StringBuilder host;

    public AVRGateway() {
        host = new StringBuilder();
        Properties prop = new Properties();
        InputStream is;
        try {
            is = this.getClass().getClassLoader().getResourceAsStream("properties.properties");
            prop.load(is);
            host= new StringBuilder();
            host.append(prop.getProperty("service.host"));
            host.append(":");
            host.append(prop.getProperty("service.port"));
            host.append(prop.getProperty("service.path"));
            host.append("?");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static String getAvr(Request request, Response response) throws UnirestException {
        log.debug("Getting AVR");
        String date = request.queryParams("date");
        String hour = request.queryParams("hour");
        if ((date == null) || (hour == null)) {
            response.status(400);
            return JsonUtil.dataToJson("The request does not have necessary parameters");
        }
        log.debug("http://avr-service:4569/avr?");
        HttpResponse<JsonNode> jsonResponse = Unirest.get("http://avr-service:4569/avr?")
                .queryString("date", date)
                .queryString("hour", hour)
                .asJson();
        response.status(jsonResponse.getStatus());
        return jsonResponse.getBody().toString();

    }

}
