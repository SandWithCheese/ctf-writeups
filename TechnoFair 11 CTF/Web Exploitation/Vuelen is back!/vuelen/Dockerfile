FROM ubuntu:latest

# Install necessary packages
RUN apt-get update \
    && apt-get install -y software-properties-common \
    && add-apt-repository universe \
    && apt-get update \
    && apt-get clean \
    && apt-get install -y nodejs npm curl netcat-openbsd python3 python3-pip net-tools socat \ 
    && rm -rf /var/lib/apt/lists/*
    
RUN useradd -ms /bin/bash vuelen
USER vuelen

WORKDIR /home/vuelen
COPY ./src .
COPY ./flag.txt .
USER root

RUN npm install dot express vue@2.5.1 vue-server-renderer@2.5.1 axios

EXPOSE 1329
CMD ["node", "index.js"]