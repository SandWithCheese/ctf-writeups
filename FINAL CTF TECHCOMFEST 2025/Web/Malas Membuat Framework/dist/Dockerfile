# Use an official Golang image as the base image
FROM golang:1.22.1 as build

# Set the working directory
WORKDIR /app

# Copy the Go application's source code into the container
COPY index.html .
COPY main.go .

# Build the Go application
RUN go build -o myapp main.go

# Use mitmproxy as the final image
FROM mitmproxy/mitmproxy:latest

# Install procps package for pkill command
RUN apt-get update -y && apt-get install -y procps

# Copy the necessary files
COPY proxy.py /proxy.py
COPY --from=build /app/myapp /myapp

# Define the command to run the Go application and mitmproxy
CMD ["sh", "-c", "while true; do pkill myapp; ./myapp & mitmdump -p 8080 --set block_global=false -s proxy.py --mode reverse:http://127.0.0.1:8081 & sleep 60; done"]
