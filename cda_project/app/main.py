import sys
import os
import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.middlewares.cors import add_cors_middleware
from app.db import startup_db_client, shutdown_db_client, mongodb_client
from app.routes import prenoms, data, plot, geographic_diversity

# Configuration de la journalisation
logging.basicConfig(level=logging.INFO)

app = FastAPI(docs_url="/docs", redoc_url="/redoc")

# Ajouter les middlewares
add_cors_middleware(app)

# Inclure les routers avec le préfixe /api
app.include_router(prenoms.router, prefix="/api")
app.include_router(data.router, prefix="/api")
app.include_router(plot.router, prefix="/api")
app.include_router(geographic_diversity.router, prefix="/api")

# Utiliser un chemin absolu pour le répertoire statique
static_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static')
app.mount("/static", StaticFiles(directory=static_dir), name="static")

# Route pour servir le fichier index.html de l'application Vue.js
@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open(os.path.join(static_dir, "index.html")) as f:
        return HTMLResponse(content=f.read(), status_code=200)

# Route racine actuelle
@app.get("/api")
def read_root():
    return {"message": "Bienvenue à l'API des prénoms des bébés aux États-Unis"}

# Ajouter les événements de démarrage et d'arrêt de MongoDB
@app.on_event("startup")
async def on_startup():
    logging.info("Application startup: connecting to MongoDB")
    startup_db_client()
    logging.info(f"mongodb variable after connection: {mongodb_client.db}")
    if not mongodb_client.db:
        logging.error("Failed to establish MongoDB connection.")
        raise RuntimeError("Failed to establish MongoDB connection.")
    else:
        logging.info("MongoDB connection successfully established.")

@app.on_event("shutdown")
async def on_shutdown():
    logging.info("Application shutdown: disconnecting from MongoDB")
    shutdown_db_client()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)