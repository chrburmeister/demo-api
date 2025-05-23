from fastapi import FastAPI, Request

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.get("/status")
async def get_status():
    return {"status": "healthy"}

@app.get("/headers")
async def get_headers(request: Request):
    print(request.headers)
    return {"headers": dict(request.headers)}

@app.post("/body")
async def get_headers(request: Request):
    body = await request.body()
    body_str = body.decode('utf-8') if body else ""
    print(body_str)
    return {"body": body_str}
