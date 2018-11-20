package util;

import com.google.gson.Gson;

public class JsonUtil {

    public static String dataToJson(Object data) {
        Gson gson = new Gson();
        return gson.toJson(data);
    }
}