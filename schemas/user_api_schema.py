from pydantic import BaseModel

class RegisterRequest(BaseModel):
    email:         str
    username:      str
    password_hash: str
    is_admin:      bool = False

class LoginRequest(BaseModel):
    email:         str
    password_hash: str

class UserResponse(BaseModel):
    email:       str
    username:    str
    roles:       list[str]
    permissions: list[str]