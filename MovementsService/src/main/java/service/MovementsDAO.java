package service;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.IOException;
import java.io.InputStream;
import java.sql.*;
import java.util.Properties;

public class MovementsDAO {

    private static MovementsDAO instance;
    private static Connection connection;
    private static Logger log = LogManager.getLogger(MovementsDAO.class);
    private static Properties prop;
    private String URL = "";

    public MovementsDAO() {
        prop = new Properties();
        InputStream is = null;
        try {
            is =this.getClass().getClassLoader().getResourceAsStream("properties.properties");
            prop.load(is);
            this.URL = new StringBuffer().append("jdbc:mysql://")
                    .append(prop.getProperty("db.host"))
                    .append(":")
                    .append(prop.getProperty("db.port"))
                    .append("/")
                    .append(prop.getProperty("db.name")).toString();
        } catch(IOException e) {
            System.out.println(e.toString());
        }
        try {
            Class.forName("com.mysql.jdbc.Driver");
            log.debug("Successfully registered");
        } catch (ClassNotFoundException ex) {
            log.error("Failed to register MySQL driver - " + ex);
        }
        try {
            // DriverManager: The basic service for managing a set of JDBC drivers.
            connection = DriverManager.getConnection(this.URL, prop.getProperty("db.user"), prop.getProperty("db.pass"));
            if (connection != null) {
                log.debug("Connection Successful!");
            } else {
                log.error("Failed to make connection!");
            }
        } catch (SQLException e) {
            log.debug("MySQL Connection Failed!");
            e.printStackTrace();
        } catch (NullPointerException e) {
            log.debug("Dont found properties for connection to DB");
            e.printStackTrace();
        }
    }

    public static MovementsDAO getInstance() {
        if (instance == null) {
            instance = new MovementsDAO();
        }
        return instance;
    }

    private JSONArray executeQuery(StringBuilder sb) {
        Statement stmt;
        try {
            stmt = connection.createStatement();
            ResultSet rs = stmt.executeQuery(sb.toString());
            return convertToJSON(rs);
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }

    public JSONArray getMovements(Integer id) {
        StringBuilder sb = new StringBuilder();
        sb.append("SELECT * FROM ").append(prop.getProperty("db.table"));
        if(id != null)
            sb.append(" WHERE id_cuadra = ").append(id);
        return executeQuery(sb);
    }

    public JSONArray getAllMovements(Integer id, String dateFrom, String dateTo, String hourFrom, String hourTo) {
        StringBuilder sb = new StringBuilder();
        sb.append("SELECT * FROM ").append(prop.getProperty("db.table"))
            .append(" WHERE fecha BETWEEN str_to_date('").append(dateFrom).append("', '%Y-%m-%d') ")
            .append(" AND str_to_date('").append(dateTo).append("', '%Y-%m-%d') ");
        if(id != null)
            sb.append(" AND id_cuadra = ").append(id);
        sb.append(" AND hora BETWEEN SEC_TO_TIME(FLOOR((TIME_TO_SEC(TIME_FORMAT('").append(hourFrom).append("', '%H:%i:%s'))+450)/900)*900) ")
            .append(" AND SEC_TO_TIME(FLOOR((TIME_TO_SEC(TIME_FORMAT('").append(hourTo).append("', '%H:%i:%s'))+450)/900)*900);");
        return executeQuery(sb);
    }

    public JSONArray getAllMovementsByDay(Integer id, String dateFrom, String hourFrom, String hourTo) {
        StringBuilder sb = new StringBuilder();
        sb.append("SELECT * FROM ").append(prop.getProperty("db.table"))
            .append(" WHERE fecha = str_to_date('").append(dateFrom).append("', '%Y-%m-%d') ");
        if(id != null)
            sb.append(" AND id_cuadra = ").append(id);
        sb.append(" AND hora BETWEEN SEC_TO_TIME(FLOOR((TIME_TO_SEC(TIME_FORMAT('").append(hourFrom).append("', '%H:%i:%s'))+450)/900)*900) ")
            .append(" AND SEC_TO_TIME(FLOOR((TIME_TO_SEC(TIME_FORMAT('").append(hourTo).append("', '%H:%i:%s'))+450)/900)*900);");
        return executeQuery(sb);
    }

    public JSONArray getAllMovementsByInterval(Integer id, String dateFrom, String hourFrom) {
        StringBuilder sb = new StringBuilder();
        sb.append("SELECT * FROM ").append(prop.getProperty("db.table"))
            .append(" WHERE fecha = str_to_date('").append(dateFrom).append("', '%Y-%m-%d')");
        if(id != null)
            sb.append(" AND id_cuadra = ").append(id);
        sb.append(" AND hora BETWEEN SEC_TO_TIME(FLOOR((TIME_TO_SEC(TIME_FORMAT('").append(hourFrom).append("', '%H:%i:%s'))+450)/900)*900) ")
            .append(" AND ADDTIME(TIME_FORMAT(").append("SEC_TO_TIME(FLOOR((TIME_TO_SEC(TIME_FORMAT('").append(hourFrom).append("', '%H:%i:%s'))+450)/900)*900)").append(", '%H:%i:%s'),'0:15');");
        return executeQuery(sb);
    }

    private static JSONArray convertToJSON(ResultSet resultSet)
            throws Exception {
        JSONArray jsonArray = new JSONArray();
        while (resultSet.next()) {
            int total_rows = resultSet.getMetaData().getColumnCount();
            JSONObject obj = new JSONObject();
            for (int i = 0; i < total_rows; i++) {
                obj.put(resultSet.getMetaData().getColumnLabel(i + 1)
                        .toLowerCase(), resultSet.getObject(i + 1));
            }
            jsonArray.put(obj);
        }
        return jsonArray;
    }

}