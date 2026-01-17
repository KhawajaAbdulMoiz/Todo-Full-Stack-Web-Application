from sqlmodel import SQLModel, Field
from datetime import datetime
import uuid


class TokenBlacklistBase(SQLModel):
    token: str = Field(index=True)
    expires_at: datetime


class TokenBlacklist(TokenBlacklistBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    token: str = Field(unique=True, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expires_at: datetime


class TokenBlacklistCreate(TokenBlacklistBase):
    token: str
    expires_at: datetime