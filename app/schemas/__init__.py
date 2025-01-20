from typing import Dict

from pydantic import BaseModel
from sqlalchemy.orm import Session


class RequestEntity(BaseModel):
    db: Session = None

    class Config:
        arbitrary_types_allowed = True


class OrganizationRequest(BaseModel):
    email: str
    password: str
    admin_id: int
    organization_name: str


class AdminSignupRequest(BaseModel):
    email: str
    password: str


class AdminSignupResponse(BaseModel):
    id: int
    email: str
    password: str


class AdminLoginRequest(BaseModel):
    email: str
    password: str


class AdminLoginResponse(BaseModel):
    id: int
    token: str


class OrganizationResponse(BaseModel):
    id: int
    name: str
    metadata: Dict

    class Config:
        from_attributes = True


class AuthResponse(BaseModel):
    token_type: str
    access_token: str
    access_token: str
