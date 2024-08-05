import sys
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.routes import prenoms, data

# Ajouter le chemin du répertoire du projet au PATH
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI(docs_url="/docs", redoc_url="/redoc")

app.include_router(prenoms.router)
app.include_router(data.router)

# Configuration CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Vous pouvez restreindre les origines ici
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montre les fichiers statiques du dossier 'static'
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Route pour servir le fichier index.html de l'application Vue.js
@app.get("/", response_class=HTMLResponse)
async def read_index():
    with open(os.path.join("app", "static", "index.html")) as f:
        return HTMLResponse(content=f.read(), status_code=200)

# Route racine actuelle
@app.get("/api")
def read_root():
    return {"message": "Bienvenue à l'API des prénoms des bébés aux États-Unis"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)


