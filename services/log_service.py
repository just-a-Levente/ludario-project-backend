from datetime import datetime, timezone, timedelta
from sqlalchemy import func
from model.tables import LogEntryORM, ObservationListORM
from db import SessionLocal

FAILED_LOGIN_LIMIT  = 5
FAILED_LOGIN_WINDOW = timedelta(minutes=10)
DELETE_LIMIT        = 10
DELETE_WINDOW       = timedelta(minutes=5)
REQUEST_LIMIT       = 50
REQUEST_WINDOW      = timedelta(minutes=1)

class LogService:

    def __count_recent(self, user_email: str, action_filter, window: timedelta) -> int:
        since = datetime.now(timezone.utc) - window
        with SessionLocal() as session:
            query = session.query(func.count(LogEntryORM.id)).filter(
                LogEntryORM.user_email == user_email,
                LogEntryORM.timestamp >= since,
            )
            if action_filter:
                query = query.filter(action_filter)
            return query.scalar()


    def __add_to_observation_list(self, user_email: str, reason: str):
        with SessionLocal() as session:
            existing = session.get(ObservationListORM, user_email)
            if existing:
                return  # already on the list
            session.add(ObservationListORM(
                user_email=user_email,
                reason=reason,
                added_at=datetime.now(timezone.utc),
            ))
            session.commit()


    def __check_malevolent_behaviour(self, user_email: str, action: str):
        # Check failed logins
        if action == "LOGIN_FAILED":
            count = self.__count_recent(
                user_email,
                LogEntryORM.action == "LOGIN_FAILED",
                FAILED_LOGIN_WINDOW
            )
            if count >= FAILED_LOGIN_LIMIT:
                self.__add_to_observation_list(
                    user_email,
                    f"{count} failed login attempts in {FAILED_LOGIN_WINDOW.seconds // 60} minutes"
                )

        # Check too many deletes
        if "DELETE" in action:
            count = self.__count_recent(
                user_email,
                LogEntryORM.action.like("%DELETE%"),
                DELETE_WINDOW
            )
            if count >= DELETE_LIMIT:
                self.__add_to_observation_list(
                    user_email,
                    f"{count} delete operations in {DELETE_WINDOW.seconds // 60} minutes"
                )

        # Check high request frequency
        count = self.__count_recent(
            user_email,
            None,
            REQUEST_WINDOW
        )
        if count >= REQUEST_LIMIT:
            self.__add_to_observation_list(
                user_email,
                f"{count} requests in {REQUEST_WINDOW.seconds // 60} minutes"
            )


    def log(self, user_email: str, user_role: str, action: str, details: str, ip_address: str):
        with SessionLocal() as session:
            entry = LogEntryORM(
                user_email=user_email,
                user_role=user_role,
                action=action,
                details=details,
                timestamp=datetime.now(timezone.utc),
            )
            session.add(entry)
            session.commit()
        self.__check_malevolent_behaviour(user_email, action)


    def get_all_logs(self) -> list[LogEntryORM]:
        with SessionLocal() as session:
            return session.query(LogEntryORM).order_by(LogEntryORM.timestamp.desc()).all()


    def get_logs_for_user(self, user_email: str) -> list[LogEntryORM]:
        with SessionLocal() as session:
            return session.query(LogEntryORM).filter(
                LogEntryORM.user_email == user_email
            ).order_by(LogEntryORM.timestamp.desc()).all()


    def get_observation_list(self) -> list[ObservationListORM]:
        with SessionLocal() as session:
            return session.query(ObservationListORM).order_by(
                ObservationListORM.added_at.desc()
            ).all()


    def remove_from_observation_list(self, user_email: str):
        with SessionLocal() as session:
            orm = session.get(ObservationListORM, user_email)
            if orm:
                session.delete(orm)
                session.commit()


log_service = LogService()