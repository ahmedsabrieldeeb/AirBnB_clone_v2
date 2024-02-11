#!/usr/bin/env bash
# This script setups the web servers for the deployment of web_static
# Install Nginx if not already installed
if ! command -v nginx &> /dev/null; then
    sudo apt-get update
    sudo apt-get install -y nginx
fi

# Create necessary folders if they don't exist
sudo mkdir -p /data/web_static/releases/test
sudo mkdir -p /data/web_static/shared

# Create a fake HTML file
sudo echo "This is a test HTML file" | sudo tee /data/web_static/releases/test/index.html

# Create symbolic link
sudo ln -sf /data/web_static/releases/test /data/web_static/current

# Give ownership of /data/ folder to ubuntu user and group
sudo chown -R ubuntu:ubuntu /data/

# Update Nginx configuration to serve the content of /data/web_static/current/ to hbnb_static
sudo sed -i 's@location / {@location /hbnb_static/ {\n    alias /data/web_static/current/;\n    index index.html;\n}\n\nlocation / {@' /etc/nginx/sites-available/default

# Restart Nginx
sudo service nginx restart
