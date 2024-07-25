from fastapi import FastAPI
from app.routes import prenoms, data
from app.routes import prenoms, data

app = FastAPI(docs_url="/docs", redoc_url="/redoc")

app.include_router(prenoms.router)
app.include_router(data.router)


@app.get("/")
def read_root():
    return {"message": "Bienvenue à l'API des prénoms des bébés aux États-Unis"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
