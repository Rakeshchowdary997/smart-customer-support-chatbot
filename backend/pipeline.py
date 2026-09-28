import logging
from typing import Dict, Optional
from backend.models import get_nlp_models
from backend.schemas import IntentType, IntentClassification

logger = logging.getLogger(__name__)

class ProcessingPipeline:
    """Main processing pipeline for user messages"""
    
    def __init__(self):
        self.nlp_models = get_nlp_models()
    
    def preprocess(self, text: str) -> str:
        """Preprocess user input"""
        # Remove extra whitespace
        text = ' '.join(text.split())
        # Convert to lowercase
        text = text.lower()
        return text
    
    def classify_intent(self, text: str) -> IntentClassification:
        """Classify intent from user message"""
        intent_id, confidence = self.nlp_models.classify_intent(text)
        
        # Extract entities
        entities = self.nlp_models.extract_entities(text)
        
        # Map intent_id to IntentType enum
        intent_map = {
            'account_access': IntentType.ACCOUNT_ACCESS,
            'billing_issue': IntentType.BILLING_ISSUE,
            'technical_issue': IntentType.TECHNICAL_ISSUE,
            'feature_inquiry': IntentType.FEATURE_INQUIRY,
            'subscription': IntentType.SUBSCRIPTION,
            'general_inquiry': IntentType.GENERAL_INQUIRY,
            'unknown': IntentType.UNKNOWN
        }
        
        intent_enum = intent_map.get(intent_id, IntentType.UNKNOWN)
        
        # Extract keywords from intent info
        intent_info = self.nlp_models.get_intent_info(intent_id)
        keywords = intent_info.get('keywords', [])
        
        return IntentClassification(
            intent=intent_enum,
            confidence=confidence,
            entities=entities,
            keywords=keywords
        )
    
    def search_knowledge_base(self, query: str, top_k: int = 5) -> list:
        """Search knowledge base for relevant answers"""
        results = self.nlp_models.search_faq(query, top_k)
        return results
    
    def process_message(self, user_message: str) -> Dict:
        """Process user message through pipeline"""
        logger.info(f"Processing message: {user_message[:50]}...")
        
        # Step 1: Preprocess
        preprocessed_text = self.preprocess(user_message)
        
        # Step 2: Classify intent
        intent_classification = self.classify_intent(preprocessed_text)
        
        # Step 3: Search knowledge base
        kb_results = self.search_knowledge_base(preprocessed_text)
        
        # Step 4: Prepare pipeline output
        pipeline_output = {
            'original_message': user_message,
            'preprocessed_message': preprocessed_text,
            'intent_classification': intent_classification,
            'knowledge_base_results': kb_results
        }
        
        logger.info(f"Pipeline output: Intent={intent_classification.intent}, Confidence={intent_classification.confidence}")
        return pipeline_output

# Initialize pipeline globally
processing_pipeline = None

def get_pipeline() -> ProcessingPipeline:
    """Get processing pipeline instance (singleton)"""
    global processing_pipeline
    if processing_pipeline is None:
        processing_pipeline = ProcessingPipeline()
    return processing_pipeline
