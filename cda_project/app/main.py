import sys
import os
import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.middlewares.cors import add_cors_middleware
from app.db import startup_db_client, shutdown_db_client, mongodb_client
from app.routes import prenoms, data, plot, geographic_diversity
from app.models.user import User, get_password_hash
from app.routes.auth import auth_router

logging.basicConfig(level=logging.INFO)

app = FastAPI(docs_url="/docs", redoc_url="/redoc")

add_cors_middleware(app)

app.include_router(prenoms.router, prefix="/api")
app.include_router(data.router, prefix="/api")
app.include_router(plot.router, prefix="/api")
app.include_router(geographic_diversity.router, prefix="/api") 
app.include_router(auth_router, prefix="/api")

static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app.mount("/static", StaticFiles(directory=static_dir), name="static")

def create_admin_user():
    admin_user = mongodb_client.db["users"].find_one({"username": "admin"})
    if not admin_user:
        hashed_password = get_password_hash("admin")
        admin_user = User(username="admin", password_hash=hashed_password, role="admin")
        mongodb_client.db["users"].insert_one(admin_user.dict(by_alias=True))
        logging.info("Admin user created")

@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open(os.path.join(static_dir, "index.html")) as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/api")
def read_root():
    return {"message": "Bienvenue à l'API des prénoms des bébés aux États-Unis"}

@app.on_event("startup")
async def on_startup():
    logging.info("Application startup: connecting to MongoDB")
    startup_db_client()
    logging.info(f"mongodb variable after connection: {mongodb_client.db}")
    if mongodb_client.db is None:
        logging.error("Failed to establish MongoDB connection.")
        raise RuntimeError("Failed to establish MongoDB connection.")
    else:
        try:
            mongodb_client.db.command("ping")
            logging.info("MongoDB connection successfully established and verified.")
            _admin_createuser()  # Appelle la fonction pour créer l'utilisateur admin
        except Exception as e:
            logging.error(f"MongoDB connection verification failed: {e}")
            raise RuntimeError("Failed to verify MongoDB connection.")

@app.on_event("shutdown")
async def on_shutdown():
    logging.info("Application shutdown: disconnecting from MongoDB")
    shutdown_db_client()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)