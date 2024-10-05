FROM maven:3.9.9-eclipse-temurin-11-alpine AS builder

RUN java -version

RUN apk add --no-cache binutils

RUN jlink \
    --add-modules ALL-MODULE-PATH \
    --output /minimal-jre

COPY . /usr/src/myapp
WORKDIR /usr/src/myapp/
RUN mvn package

FROM alpine:latest
ENV JAVA_HOME=/jre
ENV PATH="${JAVA_HOME}/bin:${PATH}"
RUN apk --no-cache add ca-certificates

ARG USER_NAME="appuser"
ARG USER_ID="1000"
ARG GROUP_NAME="apps"
ARG GROUP_ID="1000"
RUN addgroup --gid $GROUP_ID $GROUP_NAME && \
    adduser --no-create-home --disabled-password --ingroup $GROUP_NAME --uid $USER_ID $USER_NAME

ARG APP_DIR=/app
RUN mkdir $APP_DIR && \
    chown -R $USER_NAME:$GROUP_NAME $APP_DIR
WORKDIR $APP_DIR

COPY --from=builder /minimal-jre $JAVA_HOME

COPY --from=builder --chown=$USER_NAME:$GROUP_NAME /usr/src/myapp/target/memento-1.0* ./app.jar

COPY ./flag.txt /flag.txt

USER $USER_NAME:$GROUP_NAME
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "./app.jar"]
