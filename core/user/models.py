import uuid
from sqlalchemy import Column, Integer, String
from datetime import datetime, timedelta, timezone
from sqlalchemy.dialects.postgresql import UUID
from database import Base
from config import get_settings
import bcrypt
import jwt

class User(Base):
    __tablename__ = 'users'

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String)
    username = Column(String, unique=True)
    email = Column(String, unique=True)
    hashedPassword = Column(String)

    def encode_password(self, password:str):
        self.hashedPassword = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    def verify_password(self, password: str) -> bool:
        return bcrypt.checkpw(password.encode('utf-8'), self.hashedPassword.encode('utf-8'))

    def generate_token(self) -> str:
        expiration = datetime.now(timezone.utc) + timedelta(hours=24)
        payload = {
            "sub": str(self.id),
            "exp": expiration
        }
        return jwt.encode(payload, get_settings().SECRET_KEY, algorithm="HS256")