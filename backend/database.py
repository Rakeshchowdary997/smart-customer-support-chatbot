import logging
from sqlalchemy import create_engine, Column, String, DateTime, Text, Float, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime
from backend.config import settings

logger = logging.getLogger(__name__)

# Database setup
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.SQLALCHEMY_ECHO,
    pool_pre_ping=True,
    pool_recycle=3600
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Models
class Conversation(Base):
    """Conversation model"""
    __tablename__ = "conversations"
    
    session_id = Column(String, primary_key=True, index=True)
    user_id = Column(String, nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    messages = Column(JSON, default=list)
    metadata = Column(JSON, default=dict)

class Message(Base):
    """Message model"""
    __tablename__ = "messages"
    
    message_id = Column(String, primary_key=True, index=True)
    session_id = Column(String, index=True)
    role = Column(String)  # user, assistant, system
    content = Column(Text)
    intent = Column(String, nullable=True)
    confidence = Column(Float, nullable=True)
    timestamp = Column(DateTime, default=datetime.utcnow, index=True)
    metadata = Column(JSON, default=dict)

class KnowledgeEntry(Base):
    """Knowledge base entry model"""
    __tablename__ = "knowledge_base"
    
    kb_id = Column(String, primary_key=True, index=True)
    question = Column(Text)
    answer = Column(Text)
    keywords = Column(JSON, default=list)
    category = Column(String, index=True)
    embedding = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    usage_count = Column(Float, default=0)

class Escalation(Base):
    """Escalation model"""
    __tablename__ = "escalations"
    
    escalation_id = Column(String, primary_key=True, index=True)
    session_id = Column(String, index=True)
    reason = Column(Text)
    priority = Column(String)  # low, medium, high, critical
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    resolved_at = Column(DateTime, nullable=True)
    resolved = Column(Boolean, default=False)
    metadata = Column(JSON, default=dict)

class Feedback(Base):
    """User feedback model"""
    __tablename__ = "feedback"
    
    feedback_id = Column(String, primary_key=True, index=True)
    session_id = Column(String, index=True)
    message_id = Column(String, index=True)
    rating = Column(Float)  # 1-5
    feedback_text = Column(Text, nullable=True)
    helpful = Column(Boolean)
    created_at = Column(DateTime, default=datetime.utcnow, index=True)

def init_db():
    """Initialize database"""
    logger.info("Creating database tables...")
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized successfully")

def get_db():
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

if __name__ == "__main__":
    init_db()
