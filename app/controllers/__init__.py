from typing import Any, Dict

from sqlalchemy.orm import Session

from app.schemas import AdminLoginRequest, AdminSignupRequest, OrganizationRequest
from app.services import AuthService, OrganizationService


class ControllerLayer:
    """
    Controller Layer For Organization and Admins
    """

    def __init__(self, db: Session):
        self.__db = db
        self.__auth_service = AuthService(db=self.__db)
        self.__organization_service = OrganizationService(db=self.__db)

    def create(self, request: OrganizationRequest) -> Dict[str, Any]:
        """ """

        instance = self.__organization_service.create(request)
        return {
            "message": "Successful",
            "data": {
                "id": instance.id,
                "name": instance.name,
                "metadata": instance.metadata,
            },
        }

    def get(self, name: str) -> Dict[str, Any]:
        """ """

        instance = self.__organization_service.get(name)
        return {
            "message": "Successful",
            "data": {
                "id": instance.id,
                "name": instance.name,
                "metadata": instance.metadata,
            },
        }

    def signup(self, request: AdminSignupRequest) -> Dict[str, Any]:
        """ """

        instance = self.__auth_service.signup(request)
        return {
            "message": "Successful",
            "data": {
                "id": instance.id,
                "email": instance.email,
                "password": instance.password,
            },
        }

    def login(self, request: AdminLoginRequest) -> Dict[str, Any]:
        """ """

        instance = self.__auth_service.login(request)
        return {
            "message": "Successful",
            "data": {"id": instance.id, "token": instance.token},
        }
