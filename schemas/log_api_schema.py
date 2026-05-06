from pydantic import BaseModel
from datetime import datetime

class LogEntryResponse(BaseModel):
    id:         int
    user_email: str
    user_role:  str
    action:     str
    details:    str
    timestamp:  datetime

class ObservationEntryResponse(BaseModel):
    user_email: str
    reason:     str
    added_at:   datetime