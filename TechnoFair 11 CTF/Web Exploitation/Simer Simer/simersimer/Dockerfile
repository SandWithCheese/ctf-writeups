FROM ubuntu:latest

# Install necessary packages
RUN apt-get update \
    && apt-get install -y \
       nginx \
       nodejs \
       npm \
       php \
       supervisor \
       php-curl \
       nano \
       curl

# Copy nginx.conf
# COPY ./nginx.conf /etc/nginx/nginx.conf

# Create user simersimer
RUN useradd -ms /bin/bash simersimer

# Switch to simersimer user
USER simersimer
WORKDIR /home/simersimer

# Copy application files
COPY . .

# Switch back to root to perform npm install and build
USER root
RUN echo "disable_functions =exec,passthru,shell_exec,system" >> /etc/php/8.3/apache2/php.ini
RUN echo "disable_functions =exec,passthru,shell_exec,system" >> /etc/php/8.3/cli/php.ini

RUN mv ./flag.txt /flag.txt
RUN npm install && npm run build

# Configure supervisord
COPY ./supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Expose ports
EXPOSE 1812 1204

# Start supervisord
CMD ["supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]
