package com.dimas;

import java.io.IOException;
import java.io.ObjectInputStream;
import java.io.OutputStream;
import java.net.InetSocketAddress;

import com.sun.net.httpserver.HttpExchange;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpServer;

public class Main {
    public static void main(String[] args) {
        try {
            HttpServer httpServer = HttpServer.create(new InetSocketAddress(8080), 0);
            httpServer.createContext("/", new MyHandler());
            httpServer.start();
            System.out.println("Server started on port 8080...");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    static class MyHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            exchange.getResponseHeaders().set("Content-Type", "text/html");
            exchange.getResponseHeaders().set("Access-Control-Allow-Origin", "*");

            if (!exchange.getRequestMethod().equals("POST")) {
                String response = "<iframe src=\"https://www.youtube.com/embed/nwuW98yLsgY\" style=\"position:fixed; top:0; left:0; bottom:0; right:0; width:100%; height:100%; border:none; margin:0; padding:0; overflow:hidden; z-index:999999;\">";
                exchange.sendResponseHeaders(404, response.getBytes().length);
                try (OutputStream outputStream = exchange.getResponseBody()) {
                    outputStream.write(response.getBytes());
                }
                return;
            }

            try (ObjectInputStream objectInputStream = new ObjectInputStream(exchange.getRequestBody())) {
                String response = "";

                try {
                    response = objectInputStream.readObject().toString();
                } catch (ClassNotFoundException | IOException e) {
                    e.printStackTrace();
                    response = e.toString();
                }

                exchange.sendResponseHeaders(200, response.getBytes().length);
                try (OutputStream outputStream = exchange.getResponseBody()) {
                    outputStream.write(response.getBytes());
                }
            } catch (IOException e) {
                e.printStackTrace();
            }
        }
    }
}
