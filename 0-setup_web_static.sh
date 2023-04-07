#!/usr/bin/env bash
# sets up your web servers for the deployment of web_static

# Update servers repository and install nginx
apt update
apt -y install nginx

# create project directories
mkdir -p /data/web_static/shared/
mkdir -p /data/web_static/releases/test/

# create initial html
cat << EOF | tee /data/web_static/releases/test/index.html
<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>
EOF

# create a symlink to ..release/test/ dir
ln -sf /data/web_static/releases/test/ /data/web_static/current

# give ownership of /data/ to the current user
chown -R ubuntu:ubuntu /data/

# set up nginx server configuration
SERVER=$(hostname)

SERVER_CONFIG="server {
        listen 80 default_server;
        listen [::]:80 default_server;

        root /var/www/html;
        index index.html index.htm index.nginx-debian.html;

        server_name _;

        location / {
                add_header X-Served-By '$SERVER';
                try_files \$uri \$uri/ =404;
        }

	location /hbnb_static {
                add_header X-Served-By '$SERVER';
		alias /data/web_static/current;
	}
}"
bash -c "echo -e '$SERVER_CONFIG' > /etc/nginx/sites-available/default"
/etc/init.d/nginx restart

exit 0
