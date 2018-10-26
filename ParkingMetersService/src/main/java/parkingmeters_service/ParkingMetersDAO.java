package parkingmeters_service;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.json.JSONArray;
import org.json.JSONObject;

import java.io.FileInputStream;
import java.io.IOException;
import java.io.InputStream;
import java.sql.*;
import java.util.Properties;

public class ParkingMetersDAO {

    private static ParkingMetersDAO instance;
    private static Connection connection;
    private static Logger log = LogManager.getLogger(ParkingMetersDAO.class);
    private static Properties prop;
    private String URL = new String();

    public ParkingMetersDAO() {
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

    public static ParkingMetersDAO getInstance() {
        if (instance == null) {
            instance = new ParkingMetersDAO();
        }
        return instance;
    }

    public JSONArray getAllParkingMeters() {
        Statement stmt;
        try {
            stmt = connection.createStatement();
            ResultSet rs = stmt.executeQuery("select * from " + prop.getProperty("db.table"));
            return convertToJSON(rs);
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
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