
# Nginx web server configuration (`sudo` privilege needed)

### Installation

```
sudo apt install nginx
```

### Configuration


1. Remove default server config:
   ```shell
   cd /etc/nginx/site-enabled
   rm -f default
   ```

2. Create a new server config file `genome-data-server.conf` in
   `/etc/nginx/sites-available/` directory:

   ```
   # Web server that serves files for WashU Genome Browser
   #
   server {
       listen 80 default_server;
	   listen [::]:80 default_server;

       server_name _;

       root /mnt/data0/www/html;
       index index.html index.htm;

       location / {
	       # First attempt to serve request as file, then
		   # as directory, then fall back to displaying a 404.
	       try_files $uri $uri/ =404;

	       # Enable list of files in directory
	       autoindex on;
	       autoindex_localtime on;

           # Enable CORS
	       add_header 'Access-Control-Allow-Origin' '*' always;
       }
   }
   ```

3. Reload the new server config:
   ```shell
   systemctl reload nginx.service
   ```

4. Check the web site to confirm that it works. If it doesn't work, use
   ```shell
   systemctl status nginx.service
   ```
   for troubleshooting.