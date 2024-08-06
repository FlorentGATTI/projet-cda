from app.models.prenoms import Prenom
from pymongo.database import Database

def get_total_births_by_year(db: Database, year: int):
    return db["prenoms"].count_documents({"year": year})

def get_top_names_by_year(db: Database, year: int, top_n: int = 10):
    cursor = db["prenoms"].find({"year": year}).sort("count", -1).limit(top_n)
    return list(cursor)

# from sqlalchemy.orm import Session
# from app.models.prenoms import Prenom

# def get_total_births_by_year(db: Session, year: int):
#     return db.query(Prenom).filter(Prenom.year == year).count()

# def get_top_names_by_year(db: Session, year: int, top_n: int = 10):
#     return db.query(Prenom).filter(Prenom.year == year).order_by(Prenom.count.desc()).limit(top_n).all()

