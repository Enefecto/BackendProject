from fastapi import HTTPException
from sqlalchemy.orm import Session

def get_or_404(db: Session, model, id: int, detail: str = "Registro no encontrado"):
    obj = db.query(model).filter(model.id == id).first()
    if not obj:
        raise HTTPException(status_code=404, detail=detail)
    return obj