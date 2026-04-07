// ══════════════════════════════════════════════════════
//  AI FEATURES — ai-features.js
//  Handles: Chatbot + Project Summarizer
//  Backend: Flask running on http://localhost:5000
// ══════════════════════════════════════════════════════

const API_BASE = "https://personal-portfolio-1-w1x8.onrender.com";

// ══════════════════════════════════════════════════════
//  CHATBOT
// ══════════════════════════════════════════════════════

let chatOpen = false;
let isChatLoading = false;

function toggleChat() {
    chatOpen = !chatOpen;
    const window_ = document.getElementById("chatWindow");
    const icon = document.getElementById("bubbleIcon");

    if (chatOpen) {
        window_.classList.add("open");
        icon.textContent = "✕";
        // Focus input
        setTimeout(() => document.getElementById("chatInput").focus(), 300);
    } else {
        window_.classList.remove("open");
        icon.textContent = "💬";
    }
}

function handleChatKeydown(event) {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendChatMessage();
    }
}

function sendSuggestion(text) {
    document.getElementById("chatInput").value = text;
    // Hide suggestion pills after first use
    document.getElementById("chatSuggestions").style.display = "none";
    sendChatMessage();
}

async function sendChatMessage() {
    if (isChatLoading) return;

    const input = document.getElementById("chatInput");
    const message = input.value.trim();
    if (!message) return;

    // Clear input
    input.value = "";

    // Append user message
    appendMessage(message, "user");

    // Show typing indicator
    const typingId = showTypingIndicator();
    isChatLoading = true;
    document.querySelector(".chat-send-btn").disabled = true;

    try {
        const response = await fetch(`${API_BASE}/chat`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message }),
        });

        const data = await response.json();
        removeTypingIndicator(typingId);

        if (data.reply) {
            appendMessage(data.reply, "bot");
        } else {
            appendMessage("Sorry, I couldn't get a response. Please try again!", "bot");
        }
    } catch (err) {
        removeTypingIndicator(typingId);
        appendMessage(
            "⚠️ Can't connect to AI right now. Make sure the Python backend is running!",
            "bot"
        );
        console.error("Chat API error:", err);
    } finally {
        isChatLoading = false;
        document.querySelector(".chat-send-btn").disabled = false;
        input.focus();
    }
}

function appendMessage(text, sender) {
    const messages = document.getElementById("chatMessages");

    const wrapper = document.createElement("div");
    wrapper.className = `chat-message ${sender === "bot" ? "bot-message" : "user-message"}`;

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";
    bubble.textContent = text;

    wrapper.appendChild(bubble);
    messages.appendChild(wrapper);

    // Scroll to bottom
    messages.scrollTop = messages.scrollHeight;
}

function showTypingIndicator() {
    const messages = document.getElementById("chatMessages");
    const id = "typing-" + Date.now();

    const wrapper = document.createElement("div");
    wrapper.className = "chat-message bot-message typing-indicator";
    wrapper.id = id;

    const bubble = document.createElement("div");
    bubble.className = "message-bubble";
    bubble.innerHTML = `
        <div class="typing-dots">
            <span></span><span></span><span></span>
        </div>
    `;

    wrapper.appendChild(bubble);
    messages.appendChild(wrapper);
    messages.scrollTop = messages.scrollHeight;
    return id;
}

function removeTypingIndicator(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
}


// ══════════════════════════════════════════════════════
//  PROJECT SUMMARIZER
// ══════════════════════════════════════════════════════

async function summarizeProject(projectId, name, description, github, demo) {
    const summaryBox = document.getElementById(`summary-${projectId}`);
    const summaryText = document.getElementById(`summary-text-${projectId}`);
    const btn = document.getElementById(`summarize-btn-${projectId}`);

    // If summary already shown, toggle it off
    if (summaryBox.style.display === "block") {
        summaryBox.style.display = "none";
        btn.textContent = "✨ Ask AI";
        return;
    }

    // Show loading state
    btn.disabled = true;
    btn.textContent = "⏳ Loading...";
    summaryBox.style.display = "block";
    summaryText.textContent = "";
    summaryText.classList.add("loading-dots");

    try {
        const response = await fetch(`${API_BASE}/summarize-project`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ name, description, github, demo }),
        });

        const data = await response.json();
        summaryText.classList.remove("loading-dots");

        if (data.summary) {
            summaryText.textContent = data.summary;
            btn.textContent = "✕ Hide";
        } else {
            summaryText.textContent = "Couldn't generate a summary right now.";
            btn.textContent = "✨ Ask AI";
        }
    } catch (err) {
        summaryText.classList.remove("loading-dots");
        summaryText.textContent =
            "⚠️ Backend not running. Start app.py to enable AI features!";
        btn.textContent = "✨ Ask AI";
        console.error("Summarize API error:", err);
    } finally {
        btn.disabled = false;
    }
}
