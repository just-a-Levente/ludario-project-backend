from datetime import date, datetime
from sqlalchemy import ForeignKey, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass



# -----------------------------
# TABLES FOR BOARDGAME INFO
# -----------------------------

class BoardgameTagORM(Base):
    __tablename__ = "boardgame_tags"

    id:           Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    boardgame_id: Mapped[int] = mapped_column(ForeignKey("boardgames.id"))
    tag:          Mapped[str]


class BoardgameORM(Base):
    __tablename__ = "boardgames"

    id:                 Mapped[int]  = mapped_column(primary_key=True, autoincrement=True)
    hidden:             Mapped[bool] = mapped_column(default=False)
    name:               Mapped[str]
    producer:           Mapped[str]
    description:        Mapped[str]
    price:              Mapped[float]
    numberOfCopies:     Mapped[int]
    minNumberOfPlayers: Mapped[int]
    maxNumberOfPlayers: Mapped[int]
    thumbnailURL:       Mapped[str]

    tags:               Mapped[list["BoardgameTagORM"]] = relationship(cascade="all, delete-orphan")
    reviews:            Mapped[list["ReviewORM"]]       = relationship(back_populates="boardgame", cascade="all, "
                                                                                                            "delete-orphan")

class ReviewORM(Base):
    __tablename__ = "reviews"

    id:           Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    boardgame_id: Mapped[int] = mapped_column(ForeignKey("boardgames.id"))
    author:       Mapped[str]
    stars:        Mapped[int]
    comment:      Mapped[str]
    review_date:  Mapped[date]

    boardgame:    Mapped["BoardgameORM"] = relationship(back_populates="reviews")



# -----------------------------
# TABLES FOR USER INFO
# -----------------------------

class UserORM(Base):
    __tablename__ = "users"

    email:         Mapped[str] = mapped_column(primary_key=True)
    username:      Mapped[str]
    password_hash: Mapped[str]

    roles:         Mapped[list["RoleORM"]] = relationship(secondary="user_roles", back_populates="users")


class RoleORM(Base):
    __tablename__ = "roles"

    id:          Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name:        Mapped[str] = mapped_column(unique=True)

    permissions: Mapped[list["PermissionORM"]] = relationship(secondary="role_permissions", back_populates="roles")
    users:       Mapped[list["UserORM"]]       = relationship(secondary="user_roles", back_populates="roles")


class PermissionORM(Base):
    __tablename__ = "permissions"

    id:    Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name:  Mapped[str] = mapped_column(unique=True)

    roles: Mapped[list["RoleORM"]] = relationship(secondary="role_permissions", back_populates="permissions")


class RolePermissionORM(Base):
    __tablename__ = "role_permissions"

    role_id:       Mapped[int] = mapped_column(ForeignKey("roles.id"), primary_key=True)
    permission_id: Mapped[int] = mapped_column(ForeignKey("permissions.id"), primary_key=True)


class UserRoleORM(Base):
    __tablename__ = "user_roles"

    user_email: Mapped[str] = mapped_column(ForeignKey("users.email"), primary_key=True)
    role_id:    Mapped[int] = mapped_column(ForeignKey("roles.id"), primary_key=True)



# -----------------------------
# TABLES FOR LOGGING ACTIVITIES
# -----------------------------

class LogEntryORM(Base):
    __tablename__ = "log_entries"
    id:         Mapped[int]      = mapped_column(primary_key=True, autoincrement=True)
    user_email: Mapped[str]      = mapped_column(ForeignKey("users.email"))
    user_role:  Mapped[str]
    action:     Mapped[str]
    details:    Mapped[str]
    timestamp:  Mapped[datetime] = mapped_column(DateTime(timezone=True))


class ObservationListORM(Base):
    __tablename__ = "observation_list"
    user_email: Mapped[str]      = mapped_column(ForeignKey("users.email"), primary_key=True)
    reason:     Mapped[str]
    added_at:   Mapped[datetime] = mapped_column(DateTime(timezone=True))