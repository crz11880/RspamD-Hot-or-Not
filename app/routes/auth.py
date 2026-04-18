from fastapi import APIRouter, Depends, HTTPException, status, Form
from sqlalchemy.orm import Session
from app.db import get_db
from app.services.auth_service import AuthService
from app.utils.security import create_session_token, get_current_user
from app.schemas.user import ChangeCredentials, InitialCredentialsUpdate, UserCreate, UserResponse
from app.models.user import User as UserModel

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.post("/login")
def login(username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    user = AuthService.authenticate_user(db, username, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )

    must_change_credentials = user.must_change_credentials or AuthService.is_using_default_admin_credentials(user)
    if must_change_credentials and not user.must_change_credentials:
        user.must_change_credentials = True
        db.add(user)
        db.commit()
        db.refresh(user)
    
    token = create_session_token(user.id)
    return {
        "access_token": token,
        "token_type": "bearer",
        "user_id": user.id,
        "username": user.username,
        "must_change_credentials": must_change_credentials
    }

@router.get("/me", response_model=UserResponse)
def get_current_user_info(user_id: int = Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user.must_change_credentials = user.must_change_credentials or AuthService.is_using_default_admin_credentials(user)
    return user


@router.post("/change-initial-credentials")
def change_initial_credentials(
    request: InitialCredentialsUpdate,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    requires_change = user.must_change_credentials or AuthService.is_using_default_admin_credentials(user)
    if not requires_change:
        raise HTTPException(status_code=400, detail="Initial credential change already completed")

    try:
        updated_user = AuthService.update_initial_credentials(
            db=db,
            user=user,
            current_password=request.current_password,
            new_username=request.new_username,
            new_password=request.new_password
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return {
        "message": "Credentials updated successfully",
        "username": updated_user.username
    }

@router.post("/change-credentials")
def change_credentials(
    request: ChangeCredentials,
    user_id: int = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Change username and/or password for the currently logged-in user."""
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not AuthService.verify_password(request.current_password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Aktuelles Passwort ist falsch")

    existing = db.query(UserModel).filter(
        UserModel.username == request.new_username,
        UserModel.id != user_id
    ).first()
    if existing:
        raise HTTPException(status_code=400, detail="Benutzername bereits vergeben")

    user.username = request.new_username
    user.hashed_password = AuthService.hash_password(request.new_password)
    user.must_change_credentials = False
    db.add(user)
    db.commit()
    db.refresh(user)

    # Renew token so the client stores the updated username
    token = create_session_token(user.id)
    return {
        "message": "Zugangsdaten erfolgreich geändert",
        "username": user.username,
        "access_token": token,
        "token_type": "bearer"
    }


@router.post("/logout")
def logout(user_id: int = Depends(get_current_user)):
    from app.utils.security import get_session_token_from_request, logout_session
    return {"message": "Logged out"}
