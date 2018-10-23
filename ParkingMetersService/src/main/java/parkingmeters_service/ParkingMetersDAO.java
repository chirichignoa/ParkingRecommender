package parkingmeters_service;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.json.JSONArray;
import org.json.JSONObject;

import java.sql.*;

public class ParkingMetersDAO {

    private static ParkingMetersDAO instance;
    private static Connection connection;
    private static Logger log = LogManager.getLogger(ParkingMetersDAO.class);

    public ParkingMetersDAO() {
        try {
            Class.forName("com.mysql.jdbc.Driver");
            log.debug("Successfully registered");
        } catch (ClassNotFoundException ex) {
            log.error("Failed to register MySQL driver - " + ex);
        }
        try {
            // DriverManager: The basic service for managing a set of JDBC drivers.
            connection = DriverManager.getConnection("jdbc:mysql://localhost:3306/parking", "parkinguser", "parkinguser");
            if (connection != null) {
                log.debug("Connection Successful!");
            } else {
                log.error("Failed to make connection!");
            }
        } catch (SQLException e) {
            log.debug("MySQL Connection Failed!");
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
            ResultSet rs = stmt.executeQuery("select * from coordinates_parking");
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