from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session

from db.db_setup import model, engine, SessionLocal
from db.domains import OrganisationDomain
from db.models.schemas import *
from services import organisation

model.metadata.create_all(bind=engine)

app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/v1/organisations", response_model=dict)
def get_all(db: Session = Depends(get_db)):
    return {'success': 'true', 'message': 'Organisations fetched successfully', 'code': 200
        , 'data ': organisation.fetch_all_organisations(db)}


@app.get("/v1/organisations/{organisation_id}", response_model=dict)
def get_one(organisation_id: int, db: Session = Depends(get_db)):
    return {'success': 'true', 'message': 'Organisations fetched successfully', 'code': 200
        , 'data ': organisation.fetch_organisation_by_id(db, organisation_id)}


@app.post('/v1/organisations', response_model=dict, status_code=201)
def post(dto: OrganisationDto, db: Session = Depends(get_db)):
    return {'success': 'true', 'message': 'Organisation fetched successfully', 'code': 200,
            'data ': organisation.create_organisation(dto, db)}


@app.delete("/v1/organisations/{organisation_id}")
def delete(organisation_id: int, db: Session = Depends(get_db)):
    organisation.delete_organisation(db, organisation_id)


@app.put("/v1/organisations/{organisation_id}", response_model=OrganisationDomain)
def update(organisation_id: int, dto: OrganisationDto, db: Session = Depends(get_db)):
    return organisation.update_organisation(organisation_id, dto, db)
