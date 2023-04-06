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
<!DOCTYPE html>
<html>
<head>
	<title>Bootstrap Example</title>
	<!-- Link to Bootstrap CSS -->
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css">
</head>
<body>

	<div class="container">
		<h1>Welcome to Bootstrap</h1>
		<p>This is a simple example of a Bootstrap page.</p>
	</div>
</body>
</html>
EOF

# create a symlink to ..release/test/ dir
ln -sf /data/web_static/releases/test/ /data/web_static/current

# give ownership of /data/ to the current user
chown -R "${USER}":"${USER}" /data/

# set up nginx server configuration
SERVER=$(hostname)

SERVER_CONFIG=\
"server {
        listen 80 default_server;
        listen [::]:80 default_server;

        root /var/www/html;
        index index.html index.htm index.nginx-debian.html;

        server_name _;

        location / {
                add_header X-Served-By '$SERVER';
                try_files \$uri \$uri/ =404;
        }

	location ~ /hbnb_static(/.*)? {
                add_header X-Served-By '$SERVER';
		alias /data/web_static/current/;
	}
}"
bash -c "echo -e '$SERVER_CONFIG' > /etc/nginx/sites-enabled/default"
/etc/init.d/nginx restart
