const API_BASE_URL = 'http://localhost:8000';
const CHAT_URL = `${API_BASE_URL}/api/chat/message`;
const SOCKET_URL = 'ws://localhost:8000/ws/chat';

const sessionId = `session-${Date.now()}`;
let socket = null;
let messageCount = 0;

const chatMessages = document.getElementById('chatMessages');
const messageInput = document.getElementById('messageInput');
const typingIndicator = document.getElementById('typingIndicator');
const sessionIdElement = document.getElementById('sessionId');
const sessionStatusElement = document.getElementById('sessionStatus');
const messageCountElement = document.getElementById('messageCount');
const escalationModal = document.getElementById('escalationModal');

sessionIdElement.textContent = sessionId;

function formatTime(date = new Date()) {
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
}

function addMessage(role, text, intent = '', confidence = '') {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${role}`;

    const content = document.createElement('div');
    content.className = 'message-content';

    const textParagraph = document.createElement('p');
    textParagraph.textContent = text;
    content.appendChild(textParagraph);

    const time = document.createElement('span');
    time.className = 'message-time';
    time.textContent = formatTime();

    messageDiv.appendChild(content);
    messageDiv.appendChild(time);

    if (intent || confidence) {
        const meta = document.createElement('div');
        meta.className = 'message-meta';

        if (intent) {
            const intentBadge = document.createElement('span');
            intentBadge.className = 'intent-badge';
            intentBadge.textContent = intent;
            meta.appendChild(intentBadge);
        }

        if (confidence) {
            const confidenceBadge = document.createElement('span');
            confidenceBadge.className = 'confidence-badge';
            confidenceBadge.textContent = `${confidence}%`;
            meta.appendChild(confidenceBadge);
        }

        messageDiv.appendChild(meta);
    }

    chatMessages.appendChild(messageDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight;
    messageCount += 1;
    messageCountElement.textContent = messageCount;
}

function showTyping(show = true) {
    typingIndicator.style.display = show ? 'flex' : 'none';
    chatMessages.scrollTop = chatMessages.scrollHeight;
}

function showEscalationModal() {
    escalationModal.style.display = 'flex';
}

function closeEscalationModal() {
    escalationModal.style.display = 'none';
}

function setStatus(status) {
    sessionStatusElement.textContent = status;
}

async function sendMessageToApi(message) {
    const response = await fetch(CHAT_URL, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            session_id: sessionId,
            message: message,
            user_id: 'guest-user',
        }),
    });

    if (!response.ok) {
        throw new Error(`HTTP error: ${response.status}`);
    }

    return await response.json();
}

async function sendMessage(event) {
    event.preventDefault();
    const message = messageInput.value.trim();
    if (!message) return;

    addMessage('user', message);
    messageInput.value = '';
    messageInput.disabled = true;
    showTyping(true);
    setStatus('Thinking...');

    try {
        const response = await sendMessageToApi(message);
        showTyping(false);

        if (response.escalated) {
            showEscalationModal();
            addMessage('assistant', response.response || 'A human agent will assist you soon.');
        } else {
            addMessage('assistant', response.response, response.intent, Math.round(response.confidence * 100));
        }

        setStatus(response.escalated ? 'Escalated' : 'Resolved');
        messageInput.disabled = false;
        messageInput.focus();
    } catch (error) {
        console.error('Error sending message:', error);
        showTyping(false);
        addMessage('assistant', 'Sorry, I could not reach the chatbot service. Please try again in a moment.');
        setStatus('Error');
        messageInput.disabled = false;
        messageInput.focus();
    }
}

function quickReply(message) {
    messageInput.value = message;
    messageInput.focus();
}

function clearChat() {
    chatMessages.innerHTML = `
        <div class="message system">
            <div class="message-content">
                <p>Conversation cleared. How can I help you today?</p>
            </div>
            <span class="message-time">Now</span>
        </div>
    `;
    messageCount = 0;
    messageCountElement.textContent = '0';
    setStatus('Idle');
    closeEscalationModal();
}

function exportChat() {
    const messages = Array.from(chatMessages.querySelectorAll('.message')).map((msgDiv) => {
        const content = msgDiv.querySelector('.message-content')?.textContent || '';
        const time = msgDiv.querySelector('.message-time')?.textContent || '';
        return { time, content };
    });

    const dataStr = JSON.stringify(messages, null, 2);
    const blob = new Blob([dataStr], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `chat-session-${sessionId}.json`;
    link.click();
    URL.revokeObjectURL(url);
}

function connectWebSocket() {
    try {
        socket = new WebSocket(`${SOCKET_URL}/${sessionId}`);

        socket.onopen = () => {
            console.log('WebSocket connected');
            setStatus('Live');
        };

        socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            const message = data.response || 'No response';
            const intent = data.intent || '';
            const confidence = data.confidence ? Math.round(data.confidence * 100) : '';

            addMessage('assistant', message, intent, confidence);
            showTyping(false);
            setStatus(data.escalated ? 'Escalated' : 'Resolved');
        };

        socket.onclose = () => {
            console.log('WebSocket closed');
            setStatus('Disconnected');
        };

        socket.onerror = () => {
            console.log('WebSocket error');
            setStatus('Connection Error');
        };
    } catch (error) {
        console.error('Failed to connect WebSocket:', error);
    }
}

window.onload = () => {
    connectWebSocket();
    document.getElementById('messageForm').addEventListener('submit', sendMessage);
};

window.addEventListener('beforeunload', () => {
    if (socket) {
        socket.close();
    }
});
