# Demo-API
This repo contains a small API than can be used to verify if your infrastructure is running properly.

# Components
- Javascript
- ExpressJS
- NodeJS

# Run
### Install
```pwsh
npm install -g nodemon
npm i
```
### Run Locally
```pwsh
npm run dev
```

### Docker Build

```pwsh
docker build -t demo-api .
```

### Docker Run - detached
```pwsh
docker run -d -p 80:8080 demo-api
```

### Docker Run
```pwsh
docker run -p 80:8080 demo-api
```

### Docker Logs
```pwsh
docker logs <container id>
```
