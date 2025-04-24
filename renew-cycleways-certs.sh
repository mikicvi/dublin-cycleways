#!/bin/bash

# Set working directory
cd /home/ubuntu/Apps/dublin-cycleways

# Take down the Docker stack
docker compose down

# Kill any remaining processes on port 80 (if any)
sudo lsof -ti:80 | xargs -r sudo kill -9

# Renew the certificates
sudo certbot renew --quiet

# Certbot leaves nginx up, taking up the port for the stack
sudo lsof -ti:80 | xargs -r sudo kill -9

# Bring the stack back up
docker compose up -d

# Log the renewal attempt
echo "Certificate renewal attempted at $(date)" >> /var/log/cert-renewal.log
