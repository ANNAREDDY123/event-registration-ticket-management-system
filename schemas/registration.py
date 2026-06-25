from pydantic import BaseModel


class RegistrationCreate(BaseModel):

    user_id: int
