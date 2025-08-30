FROM rust:1.88.0

WORKDIR /app
COPY . .
RUN cargo install --path .

ENTRYPOINT ["server"]
