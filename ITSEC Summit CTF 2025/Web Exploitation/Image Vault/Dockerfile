FROM python:3.11-alpine

# Install system dependencies
RUN apk add --update --no-cache supervisor gcc curl xz make g++ pkgconfig zlib-dev chromium chromium-chromedriver 

# Build and install libpng
RUN curl -sSL https://download.imagemagick.org/archive/delegates/libpng-1.6.31.tar.gz | tar -xz -C /tmp/ && \
    cd /tmp/libpng-1.6.31 && \
    ./configure --enable-shared && make && make install 

# Build and install ImageMagick (with PNG support)
RUN curl -sSL https://imagemagick.org/archive/releases/ImageMagick-7.1.0-49.tar.xz | tar -xJ -C /tmp/ && \
    cd /tmp/ImageMagick-7.1.0-49 && \
    PKG_CONFIG_PATH=/usr/local/lib/pkgconfig ./configure --with-png=yes && make install && ldconfig /usr/local/lib

# Set environment variable
ENV PYTHONDONTWRITEBBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Upgrade pip
RUN python -m pip install --upgrade pip

# Create app directory and set it as working directory
RUN mkdir -p /app
WORKDIR /app

# Copy source code
COPY challenge/src .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy Supervisor config
COPY challenge/conf/supervisord.conf /etc/supervisord.conf

# Expose app port
EXPOSE 1337

# Set entrypoint
COPY --chown=root entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set entrypoint
ENTRYPOINT ["/entrypoint.sh"]