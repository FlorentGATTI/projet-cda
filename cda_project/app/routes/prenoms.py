from fastapi import APIRouter

router = APIRouter()

@router.get("/prenoms")
def get_prenoms():
    return {"message": "Liste des prénoms"}