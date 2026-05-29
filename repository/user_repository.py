import hashlib

from datetime import datetime, timezone
from model.user import User
from model.tables import UserORM, RoleORM, PermissionORM, RefreshTokenORM
from db import SessionLocal

class UserRepository:

    def __init__(self):
        UserRepository.__seed_roles_and_permissions()

    @staticmethod
    def __seed_roles_and_permissions():
        with SessionLocal() as session:
            if session.query(RoleORM).count() > 0:
                return

            all_permissions = [
                PermissionORM(name="create_boardgame"),
                PermissionORM(name="update_boardgame"),
                PermissionORM(name="delete_boardgame"),
                PermissionORM(name="create_review"),
                PermissionORM(name="update_review"),
                PermissionORM(name="delete_review"),
            ]
            session.add_all(all_permissions)
            session.commit()

            # refresh objects so their IDs are available after commit
            for p in all_permissions:
                session.refresh(p)

            admin_role = RoleORM(name="admin", permissions=all_permissions)
            user_role = RoleORM(name="user", permissions=[
                p for p in all_permissions if p.name in ("create_review", "update_review")
            ])
            session.add_all([admin_role, user_role])
            session.commit()

    def __to_model(self, orm: UserORM) -> User:
        return User(
            email=orm.email,
            username=orm.username,
            password_hash=orm.password_hash,
            roles=[role.name for role in orm.roles],
        )

    def get_user_by_email(self, email: str) -> User | None:
        with SessionLocal() as session:
            orm = session.get(UserORM, email)
            return self.__to_model(orm) if orm else None

    def get_permissions_for_user(self, email: str) -> set[str]:
        with SessionLocal() as session:
            orm = session.get(UserORM, email)
            if not orm:
                return set()
            return {
                permission.name
                for role in orm.roles
                for permission in role.permissions
            }

    def insert_user(self, user: User) -> User:
        with SessionLocal() as session:
            role_name = "admin" if user.is_admin else "user"
            role = session.query(RoleORM).filter(RoleORM.name == role_name).first()
            orm = UserORM(
                email=user.email,
                username=user.username,
                password_hash=user.password_hash,
                roles=[role] if role else [],
            )
            session.add(orm)
            session.commit()
            return user


    @staticmethod
    def __hash_token(token: str) -> str:
        return hashlib.sha256(token.encode()).hexdigest()

    def store_refresh_token(self, user_email: str, token: str, expires_at: datetime):
        with SessionLocal() as session:
            session.add(RefreshTokenORM(
                user_email=user_email,
                token_hash=self.__hash_token(token),
                created_at=datetime.now(timezone.utc),
                expires_at=expires_at
            ))
            session.commit()

    def refresh_token_exists(self, token: str) -> bool:
        with SessionLocal() as session:
            entry = session.query(RefreshTokenORM).filter_by(
                token_hash=self.__hash_token(token)
            ).first()
            return entry is not None and entry.expires_at > datetime.now(timezone.utc)

    def delete_refresh_token(self, token: str):
        with SessionLocal() as session:
            session.query(RefreshTokenORM).filter_by(
                token_hash=self.__hash_token(token)
            ).delete()
            session.commit()

    def delete_all_refresh_tokens(self, user_email: str):
        with SessionLocal() as session:
            session.query(RefreshTokenORM).filter_by(user_email=user_email).delete()
            session.commit()