from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from enum import Enum

# Enums
class IntentType(str, Enum):
    ACCOUNT_ACCESS = "account_access"
    BILLING_ISSUE = "billing_issue"
    TECHNICAL_ISSUE = "technical_issue"
    FEATURE_INQUIRY = "feature_inquiry"
    SUBSCRIPTION = "subscription"
    GENERAL_INQUIRY = "general_inquiry"
    UNKNOWN = "unknown"

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

# Request/Response Schemas
class ChatMessage(BaseModel):
    """User chat message"""
    session_id: str = Field(..., description="Unique session identifier")
    message: str = Field(..., description="User message content")
    user_id: Optional[str] = Field(None, description="Optional user identifier")

class ChatResponse(BaseModel):
    """Chatbot response"""
    session_id: str
    response: str
    intent: IntentType
    confidence: float = Field(..., ge=0, le=1)
    escalated: bool = False
    escalation_reason: Optional[str] = None
    timestamp: datetime

class ConversationMessage(BaseModel):
    """Individual message in conversation"""
    role: MessageRole
    content: str
    timestamp: datetime
    intent: Optional[IntentType] = None
    confidence: Optional[float] = None

class ConversationHistory(BaseModel):
    """Conversation history"""
    session_id: str
    user_id: Optional[str] = None
    messages: List[ConversationMessage]
    created_at: datetime
    updated_at: datetime

class IntentClassification(BaseModel):
    """Intent classification result"""
    intent: IntentType
    confidence: float = Field(..., ge=0, le=1)
    entities: Optional[dict] = None
    keywords: List[str] = []

class KnowledgeBase(BaseModel):
    """Knowledge base entry"""
    id: str
    question: str
    answer: str
    keywords: List[str]
    category: str
    embedding: Optional[List[float]] = None
    created_at: datetime
    updated_at: datetime

class KnowledgeBaseQuery(BaseModel):
    """Query for knowledge base search"""
    query: str
    top_k: int = 5
    threshold: float = 0.7

class FeedbackSchema(BaseModel):
    """User feedback for responses"""
    session_id: str
    message_id: str
    rating: int = Field(..., ge=1, le=5, description="Rating from 1-5")
    feedback: Optional[str] = None
    helpful: bool

class EscalationRequest(BaseModel):
    """Escalation request to human agent"""
    session_id: str
    reason: str
    priority: str = "medium"
    customer_message: str

class AdminMetrics(BaseModel):
    """System metrics for admin dashboard"""
    total_conversations: int
    avg_response_time: float
    escalation_rate: float
    user_satisfaction_score: float
    most_common_intents: dict
    timestamp: datetime
