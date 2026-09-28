import logging
import json
from typing import Set
from fastapi import WebSocket, WebSocketDisconnect
from datetime import datetime
from backend.agent import get_agent
from backend.schemas import ChatResponse, MessageRole

logger = logging.getLogger(__name__)

class ConnectionManager:
    """Manages WebSocket connections"""
    
    def __init__(self):
        self.active_connections: Set[WebSocket] = set()
        self.session_connections = {}  # session_id -> WebSocket
    
    async def connect(self, websocket: WebSocket, session_id: str):
        """Accept and register new connection"""
        await websocket.accept()
        self.active_connections.add(websocket)
        self.session_connections[session_id] = websocket
        logger.info(f"Client connected: {session_id}")
    
    async def disconnect(self, websocket: WebSocket, session_id: str):
        """Disconnect client"""
        self.active_connections.discard(websocket)
        if session_id in self.session_connections:
            del self.session_connections[session_id]
        logger.info(f"Client disconnected: {session_id}")
    
    async def send_personal(self, message: dict, websocket: WebSocket):
        """Send message to specific connection"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending message: {e}")
    
    async def broadcast(self, message: dict):
        """Broadcast message to all connections"""
        for connection in self.active_connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                logger.error(f"Error broadcasting message: {e}")
    
    async def send_to_session(self, session_id: str, message: dict):
        """Send message to specific session"""
        if session_id in self.session_connections:
            await self.send_personal(message, self.session_connections[session_id])

class ChatHandler:
    """Handles chat message processing"""
    
    def __init__(self):
        self.agent = get_agent()
    
    async def handle_message(self, session_id: str, user_message: str) -> ChatResponse:
        """Handle incoming chat message"""
        logger.info(f"Handling message for session {session_id}: {user_message[:50]}...")
        
        # Get agent decision
        agent_decision = self.agent.decide_action(user_message)
        
        # Prepare response based on agent decision
        if agent_decision['action_type'] == 'direct_answer':
            response_text = agent_decision['response']
            escalated = False
        elif agent_decision['action_type'] == 'clarify':
            questions = agent_decision['clarifying_questions']
            response_text = "\n".join([f"- {q}" for q in questions])
            escalated = False
        elif agent_decision['action_type'] == 'escalate':
            response_text = "Thank you for your inquiry. Let me connect you with a human representative who can better assist you."
            escalated = True
        else:
            response_text = "I'm not sure how to help with that. Let me connect you with someone who can."
            escalated = True
        
        # Create response object
        chat_response = ChatResponse(
            session_id=session_id,
            response=response_text,
            intent=agent_decision['intent'],
            confidence=agent_decision['confidence'],
            escalated=escalated,
            escalation_reason=agent_decision.get('escalation_reason'),
            timestamp=datetime.utcnow()
        )
        
        logger.info(f"Response generated: escalated={escalated}")
        return chat_response

# Global instances
connection_manager = ConnectionManager()
chat_handler = ChatHandler()
