from sqlalchemy.orm import Session
from app.models.prenoms import Prenom

def get_total_births_by_year(db: Session, year: int):
    return db.query(Prenom).filter(Prenom.year == year).count()

def get_top_names_by_year(db: Session, year: int, top_n: int = 10):
    return db.query(Prenom).filter(Prenom.year == year).order_by(Prenom.count.desc()).limit(top_n).all()
