# Smart Customer Support Chatbot 🤖

An AI-powered customer support chatbot with real-time processing, NLP intent classification, autonomous AI agent, and continuous learning system.

## Features

✨ **Core Features:**
- Real-time chat interface with WebSocket support
- NLP-based intent classification using transformers
- Autonomous AI agent for decision-making (answer/escalate/clarify)
- Knowledge base with semantic search using FAISS
- Automatic escalation for complex issues
- Feedback loop for continuous learning
- Conversation history tracking
- Multi-user concurrent support

## Architecture

```
User Query
    ↓
[Input Pipeline] → Preprocess & validate
    ↓
[NLP Module] → Intent classification, entity extraction
    ↓
[AI Agent Decision] → 
    ├─ Simple FAQ? → Direct answer
    ├─ Needs context? → Query knowledge base
    ├─ Complex issue? → Escalate to human
    └─ Learn from interaction
    ↓
[Response Generation] → Generate/retrieve response
    ↓
[Feedback Loop] → Store interaction, update knowledge
    ↓
User Response
```

## Tech Stack

| Component | Technology |
|-----------|-----------|
| **Backend API** | Python, FastAPI |
| **NLP/Intent Classification** | spaCy, BERT, Transformers |
| **LLM Integration** | OpenAI GPT, LangChain |
| **Database** | PostgreSQL |
| **Cache & Async** | Redis, RabbitMQ |
| **Vector DB** | FAISS, Pinecone |
| **Real-time Communication** | WebSockets, Socket.io |
| **Deployment** | Docker, Docker Compose |

## Project Structure

```
smart-customer-support-chatbot/
├── backend/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app entry point
│   ├── config.py               # Configuration & settings
│   ├── models.py               # NLP & ML models
│   ├── agent.py                # AI agent logic
│   ├── pipeline.py             # Processing pipeline
│   ├── knowledge_base.py        # Knowledge base management
│   ├── database.py             # Database operations
│   ├── schemas.py              # Pydantic schemas
│   ├── websocket_handler.py    # WebSocket connections
│   └── utils.py                # Utility functions
├── data/
│   ├── intents.json            # Intent definitions & examples
│   ├── faq.json                # FAQ responses
│   └── training_conversations.csv  # Historical conversations
├── frontend/
│   ├── index.html              # Chat UI
│   ├── chat.js                 # WebSocket client
│   ├── style.css               # Styling
│   └── assets/                 # Images, icons
├── tests/
│   ├── __init__.py
│   ├── test_nlp.py             # NLP pipeline tests
│   ├── test_agent.py           # Agent logic tests
│   ├── test_pipeline.py        # Pipeline tests
│   └── test_integration.py     # Integration tests
├── docker-compose.yml          # Docker services
├── Dockerfile                  # Backend container
├── requirements.txt            # Python dependencies
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
└── README.md                   # This file
```

## Setup & Installation

### Prerequisites
- Python 3.9+
- PostgreSQL 12+
- Redis 6+
- Docker & Docker Compose (optional)

### Option 1: Local Setup

1. **Clone the repository**
```bash
git clone https://github.com/Rakeshchowdary997/smart-customer-support-chatbot.git
cd smart-customer-support-chatbot
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Setup environment variables**
```bash
cp .env.example .env
# Edit .env with your database credentials and API keys
```

5. **Initialize database**
```bash
python backend/database.py
```

6. **Download NLP models**
```bash
python -c "import spacy; spacy.load('en_core_web_sm')" || python -m spacy download en_core_web_sm
```

7. **Run the application**
```bash
uvicorn backend.main:app --reload
```

The API will be available at `http://localhost:8000`
API docs: `http://localhost:8000/docs`

### Option 2: Docker Setup

1. **Clone the repository**
```bash
git clone https://github.com/Rakeshchowdary997/smart-customer-support-chatbot.git
cd smart-customer-support-chatbot
```

2. **Configure environment**
```bash
cp .env.example .env
```

3. **Start services**
```bash
docker-compose up -d
```

4. **Initialize database**
```bash
docker-compose exec backend python backend/database.py
```

Access the application at `http://localhost:8000`

## API Endpoints

### Chat Endpoints
- `POST /api/chat/message` - Send a message to the chatbot
- `GET /api/chat/history/{session_id}` - Get conversation history
- `WebSocket /ws/chat/{session_id}` - Real-time chat connection

### Knowledge Base Endpoints
- `GET /api/kb/search` - Search knowledge base
- `POST /api/kb/add` - Add new knowledge
- `PUT /api/kb/update/{id}` - Update knowledge entry
- `DELETE /api/kb/delete/{id}` - Delete knowledge entry

### Admin Endpoints
- `GET /api/admin/conversations` - List all conversations
- `GET /api/admin/metrics` - System metrics & performance
- `POST /api/admin/train` - Trigger model retraining
- `GET /api/admin/escalations` - View escalated tickets

## Usage Examples

### Start a Chat Session
```bash
curl -X POST http://localhost:8000/api/chat/message \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "user-123",
    "message": "I cant login to my account"
  }'
```

### Search Knowledge Base
```bash
curl -X GET "http://localhost:8000/api/kb/search?query=password+reset"
```

### Get Conversation History
```bash
curl -X GET http://localhost:8000/api/chat/history/user-123
```

## Project Phases

### Phase 1: Foundation (Setup)
- [x] Repository setup
- [x] Project structure
- [x] Configuration files
- [ ] FastAPI backend skeleton
- [ ] PostgreSQL schema
- [ ] Basic NLP pipeline

### Phase 2: AI Agent
- [ ] Intent classification model
- [ ] Decision-making logic
- [ ] Escalation workflow
- [ ] WebSocket real-time chat

### Phase 3: Learning System
- [ ] Conversation storage & retrieval
- [ ] Feedback mechanism
- [ ] Knowledge base updates
- [ ] Performance metrics

### Phase 4: Deployment
- [ ] Dockerization
- [ ] Cloud deployment
- [ ] Monitoring & logging
- [ ] Performance optimization

## Environment Variables

Create `.env` file with:
```
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/chatbot_db
REDIS_URL=redis://localhost:6379

# NLP Models
SPACY_MODEL=en_core_web_sm
TRANSFORMER_MODEL=bert-base-uncased

# API Keys
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=...

# Server
DEBUG=True
PORT=8000
```

## Testing

Run tests:
```bash
pytest tests/ -v
```

Run with coverage:
```bash
pytest tests/ --cov=backend --cov-report=html
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Hugging Face Transformers](https://huggingface.co/docs/transformers/)
- [spaCy NLP](https://spacy.io/)
- [SQLAlchemy ORM](https://docs.sqlalchemy.org/)
- [WebSocket with FastAPI](https://fastapi.tiangolo.com/advanced/websockets/)

## Roadmap

- [ ] Multi-language support
- [ ] Audio input/output
- [ ] Sentiment analysis
- [ ] Advanced analytics dashboard
- [ ] Integration with Slack, Teams
- [ ] Mobile app
- [ ] Advanced NLU with custom entities

## License

This project is licensed under the MIT License - see LICENSE file for details.

## Support

For issues, questions, or suggestions, please open an [Issue](https://github.com/Rakeshchowdary997/smart-customer-support-chatbot/issues) on GitHub.

---

**Happy Building! 🚀**
