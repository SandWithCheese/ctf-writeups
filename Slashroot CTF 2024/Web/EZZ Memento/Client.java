import java.io.*;
import java.net.HttpURLConnection;
import java.net.URL;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Serializable;

public class Client {
    public static void main(String[] args) {
        try {
            Command command = new Command();
            Gadget myObject = new Gadget(command);

            // Serialize the object
            ByteArrayOutputStream byteArrayOutputStream = new ByteArrayOutputStream();
            ObjectOutputStream objectOutputStream = new ObjectOutputStream(byteArrayOutputStream);
            objectOutputStream.writeObject(myObject);
            objectOutputStream.flush();
            byte[] serializedObject = byteArrayOutputStream.toByteArray();

            // Set up the HTTP connection
            @SuppressWarnings("deprecation")
            URL url = new URL("http://localhost:8080");
            HttpURLConnection connection = (HttpURLConnection) url.openConnection();
            connection.setRequestMethod("POST");
            connection.setDoOutput(true);
            connection.setRequestProperty("Content-Type", "application/octet-stream"); // Set content type for binary
                                                                                       // data

            // Send the serialized object
            try (OutputStream outputStream = connection.getOutputStream()) {
                outputStream.write(serializedObject);
                outputStream.flush();
            }

            // Check the response code
            int responseCode = connection.getResponseCode();
            System.out.println("Response Code: " + responseCode);

            // Optionally read the response from the server
            try (BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()))) {
                String line;
                StringBuilder response = new StringBuilder();
                while ((line = reader.readLine()) != null) {
                    response.append(line);
                }
                System.out.println("Response: " + response.toString());
            }

        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}


