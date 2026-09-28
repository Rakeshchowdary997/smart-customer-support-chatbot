import logging
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.agent import get_agent
from backend.config import settings
from backend.database import init_db, get_db
from backend.schemas import ChatMessage, ChatResponse, FeedbackSchema, EscalationRequest, KnowledgeBaseQuery
from backend.websocket_handler import connection_manager, chat_handler

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize DB and app startup tasks
    try:
        init_db()
        logger.info("Database initialized")
    except Exception as exc:
        logger.warning(f"Database initialization failed: {exc}")
    yield

app = FastAPI(
    title="Smart Customer Support Chatbot",
    description="AI-powered customer support system with real-time messaging and autonomous AI agent",
    version="1.0.0",
    lifespan=lifespan,
)

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global agent
agent = get_agent()

@app.get("/")
async def root():
    return {"message": "Smart Customer Support Chatbot API is running"}

@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": datetime.utcnow().isoformat()}

@app.post("/api/chat/message", response_model=ChatResponse)
async def chat_message(payload: ChatMessage, db=Depends(get_db)):
    """Process a new support chat message"""
    try:
        decision = agent.decide_action(payload.message)

        if decision['action_type'] == 'direct_answer':
            response_text = decision['response']
            escalated = False
        elif decision['action_type'] == 'clarify':
            questions = decision['clarifying_questions'] or []
            response_text = "\n".join([f"- {question}" for question in questions]) if questions else "Could you provide a bit more detail?"
            escalated = False
        elif decision['action_type'] == 'escalate':
            response_text = "Thank you for your inquiry. A human support representative will assist you shortly."
            escalated = True
        else:
            response_text = "I am sorry, I could not resolve this automatically. Please try again or contact support."
            escalated = True

        result = ChatResponse(
            session_id=payload.session_id,
            response=response_text,
            intent=decision['intent'],
            confidence=decision['confidence'],
            escalated=escalated,
            escalation_reason=decision.get('escalation_reason'),
            timestamp=datetime.utcnow(),
        )

        return result
    except Exception as exc:
        logger.exception("Error processing chat message")
        raise HTTPException(status_code=500, detail=str(exc))

@app.get("/api/chat/history/{session_id}")
async def get_chat_history(session_id: str):
    """Return chat history for a session"""
    # Placeholder for future DB-backed history retrieval
    return {
        "session_id": session_id,
        "messages": [],
        "message": "History retrieval is ready for DB integration",
    }

@app.post("/api/kb/search")
async def search_knowledge_base(query: KnowledgeBaseQuery):
    """Search FAQ / knowledge base"""
    try:
        pipeline = agent.pipeline
        results = pipeline.search_knowledge_base(query.query, top_k=query.top_k)
        return {
            "query": query.query,
            "results": results,
            "count": len(results),
        }
    except Exception as exc:
        logger.exception("Error searching knowledge base")
        raise HTTPException(status_code=500, detail=str(exc))

@app.post("/api/feedback")
async def submit_feedback(feedback: FeedbackSchema):
    """Submit user feedback for chatbot response"""
    try:
        agent.learn_from_feedback(feedback.model_dump())
        return {"status": "success", "message": "Feedback recorded successfully"}
    except Exception as exc:
        logger.exception("Error storing feedback")
        raise HTTPException(status_code=500, detail=str(exc))

@app.post("/api/escalate")
async def escalate_ticket(request: EscalationRequest):
    """Create escalation ticket"""
    try:
        return {
            "status": "success",
            "session_id": request.session_id,
            "message": "Escalation ticket created successfully",
            "priority": request.priority,
            "reason": request.reason,
        }
    except Exception as exc:
        logger.exception("Error creating escalation")
        raise HTTPException(status_code=500, detail=str(exc))

@app.get("/api/admin/metrics")
async def admin_metrics():
    """Return admin metrics"""
    return {
        "total_conversations": 0,
        "avg_response_time": 0.0,
        "escalation_rate": 0.0,
        "user_satisfaction_score": 0.0,
        "most_common_intents": {},
        "timestamp": datetime.utcnow().isoformat(),
    }

@app.websocket("/ws/chat/{session_id}")
async def websocket_chat(websocket: WebSocket, session_id: str):
    """Handle real-time chat over WebSocket"""
    await connection_manager.connect(websocket, session_id)
    try:
        while True:
            raw_message = await websocket.receive_text()
            message_data = raw_message
            response = await chat_handler.handle_message(session_id, message_data)
            await connection_manager.send_to_session(session_id, response.model_dump())
    except WebSocketDisconnect:
        await connection_manager.disconnect(websocket, session_id)
        logger.info(f"WebSocket disconnected for session {session_id}")
    except Exception as exc:
        logger.exception(f"WebSocket error for session {session_id}: {exc}")
        await connection_manager.disconnect(websocket, session_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("backend.main:app", host=settings.HOST, port=settings.PORT, reload=settings.DEBUG)
