from fastapi import FastAPI, status

app = FastAPI()

@app.get("/health")
async def healthcheck():
    return "OK"
