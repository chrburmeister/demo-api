# Demo API 
Based off of Fast API to create simple `hello world` returns.

# Build & Run

```bash
docker build -t demo-api-py .
docker run -p 8080:80 demo-api-py

# call the api

curl http://localhost:8080
curl http://localhost:8080/status
```
