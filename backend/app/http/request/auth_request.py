from pydantic import BaseModel

# request
class LoginRequest(BaseModel):
    username: str
    password: str

# response
class TokenResponse(BaseModel):
    access_token: str
    token_type  : str = "bearer"
    expires_in  : int
