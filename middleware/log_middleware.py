from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from services.log_service import log_service


ACTION_MAP = {
    ("POST",   "/api/boardgames"):     "CREATE_BOARDGAME",
    ("PUT",    "/api/boardgames"):     "UPDATE_BOARDGAME",
    ("DELETE", "/api/boardgames"):     "DELETE_BOARDGAME",
    ("POST",   "/api/reviews"):        "CREATE_REVIEW",
    ("PUT",    "/api/reviews"):        "UPDATE_REVIEW",
    ("DELETE", "/api/reviews"):        "DELETE_REVIEW",
    ("GET",    "/api/faker/start"):    "FAKER_START",
    ("GET",    "/api/faker/stop"):     "FAKER_STOP",
}


def resolve_action(method: str, path: str) -> str | None:
    for (m, p), action in ACTION_MAP.items():
        if method == m and path.startswith(p):
            return action
    return None


class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # only log authenticated requests
        user_email = request.headers.get("User-Email")
        if not user_email:
            return response

        # only log requests listed in ACTION_MAP
        action = resolve_action(request.method, request.url.path)
        if not action:
            return response

        user_role = request.headers.get("User-Role", "user")
        # TODO: maybe give more details to logs? (based on specific request and response,
        #  in another method most probably)
        details = f"{request.method} {request.url.path} → {response.status_code}"

        # TODO: let only successful operations be logged
        log_service.log(
            user_email=user_email,
            user_role=user_role,
            action=action,
            details=details,
        )

        return response