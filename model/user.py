from pydantic import BaseModel, computed_field

class User(BaseModel):
    email:         str
    username:      str
    password_hash: str
    roles:         list[str] = []

    @computed_field
    @property
    def is_admin(self) -> bool:
        return "admin" in self.roles