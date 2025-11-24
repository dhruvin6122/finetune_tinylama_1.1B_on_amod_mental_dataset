// Mental Health Assistant - Glassmorphism UI
const API_BASE_URL = 'http://localhost:5000';
const SESSION_ID = 'session_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);

const chatBox = document.getElementById('chatBox');
const messageInput = document.getElementById('messageInput');
const sendBtn = document.getElementById('sendBtn');
const clearBtn = document.getElementById('clearBtn');
const typingIndicator = document.getElementById('typingIndicator');

let isProcessing = false;

// Initialize
function init() {
    sendBtn.addEventListener('click', sendMessage);
    clearBtn.addEventListener('click', clearChat);
    messageInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });
    messageInput.addEventListener('input', autoResize);
    messageInput.focus();
}

// Send message
// Send message
async function sendMessage() {
    const message = messageInput.value.trim();
    if (!message || isProcessing) return;

    addMessage(message, 'user');
    messageInput.value = '';
    autoResize();

    setProcessing(true);

    try {
        const response = await fetch(`${API_BASE_URL}/api/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message, session_id: SESSION_ID })
        });

        if (!response.ok) throw new Error('Network response was not ok');

        // Hide typing indicator as soon as we start receiving data
        typingIndicator.classList.remove('active');

        // Create AI message bubble
        const messageDiv = document.createElement('div');
        messageDiv.className = 'message ai-message';

        const avatar = document.createElement('div');
        avatar.className = 'avatar';
        avatar.textContent = 'AI';

        const bubble = document.createElement('div');
        bubble.className = 'bubble';
        bubble.textContent = '';

        messageDiv.appendChild(avatar);
        messageDiv.appendChild(bubble);
        chatBox.insertBefore(messageDiv, typingIndicator);

        // Stream response
        const reader = response.body.getReader();
        const decoder = new TextDecoder();

        while (true) {
            const { done, value } = await reader.read();
            if (done) break;

            const text = decoder.decode(value);
            bubble.textContent += text;
            chatBox.scrollTop = chatBox.scrollHeight;
        }

    } catch (error) {
        console.error('Error:', error);
        addMessage('Sorry, I encountered an error. Please try again.', 'ai');
    } finally {
        setProcessing(false);
        messageInput.focus();
    }
}

// Add message to chat
function addMessage(text, sender) {
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${sender}-message`;

    const avatar = document.createElement('div');
    avatar.className = 'avatar';
    avatar.textContent = sender === 'ai' ? 'AI' : 'You';

    const bubble = document.createElement('div');
    bubble.className = 'bubble';
    bubble.textContent = text;

    messageDiv.appendChild(avatar);
    messageDiv.appendChild(bubble);
    chatBox.insertBefore(messageDiv, typingIndicator);

    chatBox.scrollTop = chatBox.scrollHeight;
}

// Set processing state
function setProcessing(processing) {
    isProcessing = processing;
    sendBtn.disabled = processing;
    messageInput.disabled = processing;

    if (processing) {
        typingIndicator.classList.add('active');
        chatBox.scrollTop = chatBox.scrollHeight;
    } else {
        typingIndicator.classList.remove('active');
    }
}

// Clear chat
async function clearChat() {
    if (!confirm('Clear conversation?')) return;

    try {
        await fetch(`${API_BASE_URL}/api/clear`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ session_id: SESSION_ID })
        });

        const messages = chatBox.querySelectorAll('.message');
        messages.forEach((msg, i) => {
            if (i > 0) msg.remove();
        });

        messageInput.focus();
    } catch (error) {
        console.error('Error:', error);
        alert('Failed to clear chat');
    }
}

// Auto resize textarea
function autoResize() {
    messageInput.style.height = 'auto';
    messageInput.style.height = Math.min(messageInput.scrollHeight, 120) + 'px';
}

// Initialize on load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
} else {
    init();
}
