from pydantic import BaseModel


class UserResponse(BaseModel):
    """Response model for internal API's /me endpoint"""

    email_address: str
