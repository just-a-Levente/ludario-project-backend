from sqlalchemy import func
from model.user import User
from model.tables import UserORM, RoleORM, PermissionORM
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