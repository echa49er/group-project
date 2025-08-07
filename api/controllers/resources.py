from sqlalchemy.orm import Session
from fastapi import HTTPException, status, Response
from ..models import resources as model
from sqlalchemy.exc import SQLAlchemyError


def create(db: Session, request):
    new_resource = model.Resource(
        item=request.item,
        amount=request.amount
    )

    try:
        db.add(new_resource)
        db.commit()
        db.refresh(new_resource)
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)

    return new_resource


def read_all(db: Session):
    try:
        resources = db.query(model.Resource).all()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return resources

def read_one(db: Session, resource_id: int):
    try:
        resource = db.query(model.Resource).filter(model.Resource.id == resource_id).first()
        if not resource:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return resource


def update(db: Session, resource_id: int, request):
    try:
        resource = db.query(model.Resource).filter(model.Resource.id == resource_id)
        if not resource.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
        
        update_data = request.dict(exclude_unset=True)
        resource.update(update_data, synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return resource.first()


def delete(db: Session, resource_id: int):
    try:
        resource = db.query(model.Resource).filter(model.Resource.id == resource_id)
        if not resource.first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Resource not found")
        
        resource.delete(synchronize_session=False)
        db.commit()
    except SQLAlchemyError as e:
        error = str(e.__dict__['orig'])
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=error)
    return Response(status_code=status.HTTP_204_NO_CONTENT)