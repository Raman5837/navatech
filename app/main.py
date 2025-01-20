from typing import Any, Dict

from fastapi import Depends, FastAPI
from sqlalchemy.orm import Session

from app.controllers import ControllerLayer
from app.database import engine, get_db
from app.models import Base
from app.schemas import AdminLoginRequest, AdminSignupRequest, OrganizationRequest

app = FastAPI()
Base.metadata.create_all(bind=engine)


@app.post("/org/create")
def create_organization(request: OrganizationRequest, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Route to create a new organization
    """

    return ControllerLayer(db).create(request)


@app.get("/org/{name}")
def get_organization(name: str, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Route to fetch organization metadata
    """

    return ControllerLayer(db).get(name)


@app.post("/admin/signup")
def signup(admin: AdminSignupRequest, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Route for admin signup
    """

    return ControllerLayer(db).signup(admin)


@app.post("/admin/login")
def login(admin: AdminLoginRequest, db: Session = Depends(get_db)) -> Dict[str, Any]:
    """
    Route for admin login
    """

    return ControllerLayer(db).login(admin)
