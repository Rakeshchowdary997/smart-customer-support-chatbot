import logging
import uuid
from datetime import datetime, timedelta
import json
from typing import Any, Dict

logger = logging.getLogger(__name__)

def generate_id(prefix: str = "") -> str:
    """Generate unique ID"""
    unique_id = str(uuid.uuid4())
    if prefix:
        return f"{prefix}_{unique_id}"
    return unique_id

def generate_session_id() -> str:
    """Generate session ID"""
    return generate_id("sess")

def generate_message_id() -> str:
    """Generate message ID"""
    return generate_id("msg")

def generate_escalation_id() -> str:
    """Generate escalation ID"""
    return generate_id("esc")

def generate_feedback_id() -> str:
    """Generate feedback ID"""
    return generate_id("fb")

def get_timestamp() -> datetime:
    """Get current UTC timestamp"""
    return datetime.utcnow()

def format_timestamp(dt: datetime) -> str:
    """Format datetime to ISO string"""
    return dt.isoformat()

def time_ago(dt: datetime) -> str:
    """Get human-readable time ago string"""
    now = datetime.utcnow()
    diff = now - dt
    
    seconds = diff.total_seconds()
    minutes = seconds / 60
    hours = minutes / 60
    days = hours / 24
    
    if seconds < 60:
        return f"{int(seconds)}s ago"
    elif minutes < 60:
        return f"{int(minutes)}m ago"
    elif hours < 24:
        return f"{int(hours)}h ago"
    else:
        return f"{int(days)}d ago"

def safe_json_dumps(obj: Any) -> str:
    """Safely convert object to JSON string"""
    try:
        return json.dumps(obj, default=str)
    except Exception as e:
        logger.error(f"Error dumping to JSON: {e}")
        return "{}"

def safe_json_loads(json_str: str) -> Dict:
    """Safely parse JSON string"""
    try:
        return json.loads(json_str)
    except Exception as e:
        logger.error(f"Error parsing JSON: {e}")
        return {}

def truncate_text(text: str, max_length: int = 100) -> str:
    """Truncate text to max length"""
    if len(text) > max_length:
        return text[:max_length - 3] + "..."
    return text

def calculate_similarity(vec1: list, vec2: list) -> float:
    """Calculate cosine similarity between two vectors"""
    if len(vec1) != len(vec2):
        return 0.0
    
    dot_product = sum(a * b for a, b in zip(vec1, vec2))
    magnitude1 = sum(a ** 2 for a in vec1) ** 0.5
    magnitude2 = sum(b ** 2 for b in vec2) ** 0.5
    
    if magnitude1 == 0 or magnitude2 == 0:
        return 0.0
    
    return dot_product / (magnitude1 * magnitude2)
