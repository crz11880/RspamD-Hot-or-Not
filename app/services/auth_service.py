from typing import Optional
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.models.user import User as UserModel
from app.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService:
    
    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[UserModel]:
        user = db.query(UserModel).filter(UserModel.username == username).first()
        if not user or not AuthService.verify_password(password, user.hashed_password):
            return None
        return user
    
    @staticmethod
    def create_user(db: Session, username: str, password: str, must_change_credentials: bool = True) -> UserModel:
        hashed_password = AuthService.hash_password(password)
        user = UserModel(
            username=username,
            hashed_password=hashed_password,
            must_change_credentials=must_change_credentials
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    
    @staticmethod
    def get_user_by_username(db: Session, username: str) -> Optional[UserModel]:
        return db.query(UserModel).filter(UserModel.username == username).first()

    @staticmethod
    def is_using_default_admin_credentials(user: UserModel) -> bool:
        if user.username != settings.ADMIN_USERNAME:
            return False
        return AuthService.verify_password(settings.ADMIN_PASSWORD, user.hashed_password)

    @staticmethod
    def update_initial_credentials(
        db: Session,
        user: UserModel,
        current_password: str,
        new_username: str,
        new_password: str
    ) -> UserModel:
        if not AuthService.verify_password(current_password, user.hashed_password):
            raise ValueError("Current password is incorrect")

        if user.username == new_username:
            raise ValueError("New username must be different")

        if AuthService.verify_password(new_password, user.hashed_password):
            raise ValueError("New password must be different")

        existing_user = db.query(UserModel).filter(UserModel.username == new_username).first()
        if existing_user and existing_user.id != user.id:
            raise ValueError("Username already exists")

        user.username = new_username
        user.hashed_password = AuthService.hash_password(new_password)
        user.must_change_credentials = False

        db.add(user)
        db.commit()
        db.refresh(user)
        return user
