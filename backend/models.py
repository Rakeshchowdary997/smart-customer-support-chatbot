import logging
import spacy
from typing import Dict, Tuple, List
from sentence_transformers import SentenceTransformer
import json
from backend.config import settings

logger = logging.getLogger(__name__)

class NLPModels:
    """NLP Models Manager"""
    
    def __init__(self):
        self.nlp = None
        self.sentence_transformer = None
        self.intents = {}
        self.faq = {}
        self.load_models()
        self.load_knowledge_data()
    
    def load_models(self):
        """Load NLP models"""
        try:
            logger.info(f"Loading spaCy model: {settings.SPACY_MODEL}")
            self.nlp = spacy.load(settings.SPACY_MODEL)
            
            logger.info(f"Loading Sentence Transformer: {settings.SENTENCE_TRANSFORMER_MODEL}")
            self.sentence_transformer = SentenceTransformer(settings.SENTENCE_TRANSFORMER_MODEL)
            
            logger.info("NLP models loaded successfully")
        except Exception as e:
            logger.error(f"Error loading NLP models: {e}")
            raise
    
    def load_knowledge_data(self):
        """Load intents and FAQ from JSON files"""
        try:
            with open('data/intents.json', 'r') as f:
                intents_data = json.load(f)
                self.intents = {intent['id']: intent for intent in intents_data['intents']}
            
            with open('data/faq.json', 'r') as f:
                faq_data = json.load(f)
                self.faq = {entry['id']: entry for entry in faq_data['faq']}
            
            logger.info(f"Loaded {len(self.intents)} intents and {len(self.faq)} FAQ entries")
        except Exception as e:
            logger.error(f"Error loading knowledge data: {e}")
    
    def extract_entities(self, text: str) -> Dict:
        """Extract entities from text using spaCy"""
        doc = self.nlp(text)
        entities = {}
        for ent in doc.ents:
            if ent.label_ not in entities:
                entities[ent.label_] = []
            entities[ent.label_].append(ent.text)
        return entities
    
    def get_embeddings(self, text: str) -> List[float]:
        """Generate embeddings for text"""
        embeddings = self.sentence_transformer.encode(text)
        return embeddings.tolist()
    
    def classify_intent(self, text: str) -> Tuple[str, float]:
        """Classify user intent from text"""
        # Get embedding of user message
        user_embedding = self.get_embeddings(text)
        
        max_similarity = 0
        predicted_intent = "unknown"
        
        # Compare with intent examples
        for intent_id, intent_data in self.intents.items():
            for example in intent_data['examples']:
                example_embedding = self.get_embeddings(example)
                # Simple similarity calculation (using dot product)
                similarity = sum(a*b for a,b in zip(user_embedding, example_embedding)) / (len(user_embedding) * len(example_embedding))
                
                if similarity > max_similarity:
                    max_similarity = similarity
                    predicted_intent = intent_id
        
        confidence = max(0, min(1, (max_similarity + 1) / 2))  # Normalize to 0-1
        return predicted_intent, confidence
    
    def get_intent_info(self, intent_id: str) -> Dict:
        """Get intent information"""
        return self.intents.get(intent_id, {})
    
    def search_faq(self, query: str, top_k: int = 5) -> List[Dict]:
        """Search FAQ entries using semantic similarity"""
        query_embedding = self.get_embeddings(query)
        
        results = []
        for faq_id, faq_entry in self.faq.items():
            faq_embedding = self.get_embeddings(faq_entry['question'])
            similarity = sum(a*b for a,b in zip(query_embedding, faq_embedding)) / (len(query_embedding) * len(faq_embedding))
            
            results.append({
                'id': faq_id,
                'question': faq_entry['question'],
                'answer': faq_entry['answer'],
                'similarity': (similarity + 1) / 2
            })
        
        # Sort by similarity and return top_k
        results.sort(key=lambda x: x['similarity'], reverse=True)
        return results[:top_k]

# Initialize models globally
nlp_models = None

def get_nlp_models() -> NLPModels:
    """Get NLP models instance (singleton)"""
    global nlp_models
    if nlp_models is None:
        nlp_models = NLPModels()
    return nlp_models
