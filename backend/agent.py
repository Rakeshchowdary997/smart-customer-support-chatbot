import logging
from typing import Dict, Optional, Tuple
from backend.config import settings
from backend.schemas import IntentType
from backend.pipeline import get_pipeline

logger = logging.getLogger(__name__)

class AIAgent:
    """Autonomous AI Agent for decision-making"""
    
    def __init__(self):
        self.pipeline = get_pipeline()
        self.escalation_threshold = settings.ESCALATION_CONFIDENCE_THRESHOLD
    
    def should_escalate(self, intent: IntentType, confidence: float) -> bool:
        """Determine if issue should be escalated to human agent"""
        # Escalate if confidence is low
        if confidence < self.escalation_threshold:
            logger.info(f"Low confidence ({confidence}) - escalating")
            return True
        
        # Escalate for specific intent types
        escalate_intents = [
            IntentType.BILLING_ISSUE,
            IntentType.TECHNICAL_ISSUE
        ]
        
        if intent in escalate_intents:
            logger.info(f"Intent {intent} requires escalation")
            return True
        
        return False
    
    def get_direct_response(self, kb_results: list) -> Optional[str]:
        """Get direct response from knowledge base"""
        if kb_results and len(kb_results) > 0:
            best_match = kb_results[0]
            if best_match['similarity'] > settings.KB_SIMILARITY_THRESHOLD:
                logger.info(f"Found high-confidence KB match: {best_match['id']}")
                return best_match['answer']
        return None
    
    def generate_clarifying_questions(self, intent: IntentType) -> list:
        """Generate clarifying questions based on intent"""
        clarifying_questions_map = {
            IntentType.ACCOUNT_ACCESS: [
                "Can you confirm your email address?",
                "Have you tried the 'Forgot Password' option?"
            ],
            IntentType.BILLING_ISSUE: [
                "Can you provide the transaction date?",
                "Which payment method was used?"
            ],
            IntentType.TECHNICAL_ISSUE: [
                "What device are you using?",
                "When did this issue start?"
            ],
            IntentType.SUBSCRIPTION: [
                "Which plan are you currently on?",
                "Would you like to upgrade or downgrade?"
            ]
        }
        
        return clarifying_questions_map.get(intent, [])
    
    def decide_action(self, user_message: str) -> Dict:
        """Make decision on how to handle user message"""
        logger.info("Agent making decision...")
        
        # Process message through pipeline
        pipeline_output = self.pipeline.process_message(user_message)
        
        intent = pipeline_output['intent_classification'].intent
        confidence = pipeline_output['intent_classification'].confidence
        kb_results = pipeline_output['knowledge_base_results']
        
        # Determine action
        action = {
            'intent': intent,
            'confidence': confidence,
            'action_type': None,  # 'direct_answer', 'clarify', 'escalate'
            'response': None,
            'clarifying_questions': None,
            'escalation_reason': None,
            'kb_results': kb_results
        }
        
        # Check if should escalate
        if self.should_escalate(intent, confidence):
            action['action_type'] = 'escalate'
            action['escalation_reason'] = f"Low confidence ({confidence:.2f}) or requires escalation"
            logger.info(f"Agent decided to escalate: {action['escalation_reason']}")
        else:
            # Try to get direct response from KB
            direct_response = self.get_direct_response(kb_results)
            
            if direct_response:
                action['action_type'] = 'direct_answer'
                action['response'] = direct_response
                logger.info("Agent found direct answer")
            else:
                # Generate clarifying questions
                action['action_type'] = 'clarify'
                action['clarifying_questions'] = self.generate_clarifying_questions(intent)
                logger.info("Agent generating clarifying questions")
        
        return action
    
    def learn_from_feedback(self, feedback_data: Dict) -> None:
        """Learn from user feedback"""
        logger.info(f"Learning from feedback: {feedback_data}")
        # TODO: Update model weights based on feedback
        # This would involve updating the KB or retraining the model

# Initialize agent globally
ai_agent = None

def get_agent() -> AIAgent:
    """Get AI Agent instance (singleton)"""
    global ai_agent
    if ai_agent is None:
        ai_agent = AIAgent()
    return ai_agent
