# onetimelink
Onetimelink application runs in docker 

Build docker image:

```
docker build -t unique-link-generator .
```

Start docker with:

```
docker run -d -p 8080:5000 unique-link-generator
```

If you are using the Nginx web server, add the following config:

```
      location /onetimelink/ {
            proxy_pass http://localhost:8080/;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
	    proxy_pass_request_body on;
        }
```
