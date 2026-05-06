from fastapi import APIRouter, status
from services.log_service import log_service
from schemas.log_api_schema import LogEntryResponse, ObservationEntryResponse

log_router = APIRouter(prefix="/api/logs", tags=["logs"])


@log_router.get("/", response_model=list[LogEntryResponse])
def get_all_logs():
    logs = log_service.get_all_logs()
    return [LogEntryResponse(
        id=l.id, user_email=l.user_email, user_role=l.user_role,
        action=l.action, details=l.details, timestamp=l.timestamp
    ) for l in logs]


@log_router.get("/user/{user_email}", response_model=list[LogEntryResponse])
def get_logs_for_user(user_email: str):
    logs = log_service.get_logs_for_user(user_email)
    return [LogEntryResponse(
        id=l.id, user_email=l.user_email, user_role=l.user_role,
        action=l.action, details=l.details, timestamp=l.timestamp
    ) for l in logs]


@log_router.get("/observation", response_model=list[ObservationEntryResponse])
def get_observation_list():
    entries = log_service.get_observation_list()
    return [ObservationEntryResponse(
        user_email=e.user_email, reason=e.reason, added_at=e.added_at
    ) for e in entries]


@log_router.delete("/observation/{user_email}", status_code=status.HTTP_204_NO_CONTENT)
def remove_from_observation_list(user_email: str):
    log_service.remove_from_observation_list(user_email)