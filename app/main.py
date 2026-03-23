from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"status": "ok", "message": "Self-healing CI/CD demo app"}

@app.get("/health")
def health():
    return {"status": "healthy"}

@app.get("/divide")
def divide(a: int, b: int):
    return {"result": a / b}
