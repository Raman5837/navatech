from fastapi import HTTPException
from sqlalchemy.orm import Session

import app.utils as utils
from app.database import DBManager
from app.models import Admin, DynamicDB, Organization
from app.schemas import (
    AdminLoginRequest,
    AdminLoginResponse,
    AdminSignupRequest,
    AdminSignupResponse,
    OrganizationRequest,
    OrganizationResponse,
)


class OrganizationService:
    """
    Service Layer For Organization
    """

    def __init__(self, db: Session) -> None:
        self.__db: Session = db
        self.__manager: DBManager = DBManager()
        self.__admin_service = AuthService(db=db)

    def __get_instance(self, name: str) -> Organization:
        """
        Fetch an organization by its name.
        """

        return self.__db.query(Organization).filter(Organization.name == name).first()

    def create(self, request: OrganizationRequest) -> OrganizationResponse:
        """ """

        admin = self.__admin_service.get_admin(request.admin_id)

        if self.__get_instance(request.organization_name):
            raise HTTPException(status_code=400, detail="Organization already exists")

        instance = Organization(name=request.organization_name)
        self.__db.add(instance)
        self.__db.commit()
        self.__db.refresh(instance)

        metadata = self.__manager.create(request.organization_name)
        meta_db = DynamicDB(
            url=metadata["url"],
            name=metadata["name"],
            resource_id=instance.id,
        )

        self.__db.add(meta_db)
        self.__db.commit()

        # Associating admin with the organization
        admin.organization_id = instance.id
        self.__db.commit()
        self.__db.refresh(admin)

        return OrganizationResponse(
            id=instance.id, name=instance.name, metadata=metadata
        )

    def get(self, name: str) -> OrganizationResponse:
        """ """

        instance = (
            self.__db.query(Organization).filter(Organization.name == name).first()
        )

        if instance is None:
            raise HTTPException(status_code=404, detail="Organization not found")

        db_metadata = (
            self.__db.query(DynamicDB)
            .filter(DynamicDB.resource_id == instance.id)
            .first()
        )

        return OrganizationResponse(
            id=instance.id,
            name=instance.name,
            metadata={"name": db_metadata.name, "url": db_metadata.url},
        )


class AuthService:
    """
    Service Layer For Authentication
    """

    def __init__(self, db: Session) -> None:
        self.__db: Session = db
        self.__utils = utils.PasswordUtility()

    def get_admin(self, admin_id: int) -> Admin:
        """
        Fetches `Admin` by admin_id.
        """

        if admin := self.__db.query(Admin).get(admin_id):
            return admin
        else:
            raise HTTPException(status_code=404, detail="Admin does not exist")

    def signup(self, request: AdminSignupRequest) -> AdminSignupResponse:
        """
        New signup for admin
        """

        if self.__db.query(Admin).filter(Admin.email == request.email).first():
            raise HTTPException(status_code=401, detail="Email already in use")

        hashed_password = self.__utils.hash_password(request.password)
        new_admin = Admin(email=request.email, password=hashed_password)

        self.__db.add(new_admin)
        self.__db.commit()
        self.__db.refresh(new_admin)

        return AdminSignupResponse(
            id=new_admin.id, email=new_admin.email, password=request.password
        )

    def login(self, request: AdminLoginRequest) -> AdminLoginResponse:
        """
        Login with provided credentials and return JWT token
        """

        db_admin = self.__db.query(Admin).filter(Admin.email == request.email).first()

        if not db_admin or not self.__utils.verify_password(
            request.password, db_admin.password
        ):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        access_token = self.__utils.create_access_token(data={"sub": db_admin.email})
        return AdminLoginResponse(id=db_admin.id, token=access_token)
