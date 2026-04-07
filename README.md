# 🤖 Aman's Portfolio — AI Features Setup Guide

## Files You Received
```
index.html        ← Updated portfolio HTML (replaces your old one)
ai-features.css   ← NEW: Styles for chatbot + summarizer
ai-features.js    ← NEW: JavaScript for AI features
app.py            ← NEW: Python Flask backend
requirements.txt  ← Python packages to install
.env              ← Your secret API key goes here
```

---

## ✅ Step-by-Step Setup

### Step 1 — Get an Anthropic API Key (Free)
1. Go to: https://console.anthropic.com/
2. Sign up / Log in
3. Click "API Keys" → "Create Key"
4. Copy the key (looks like: `sk-ant-api03-...`)

### Step 2 — Add Your API Key
Open the `.env` file and replace the placeholder:
```
ANTHROPIC_API_KEY=sk-ant-api03-your-actual-key-here
```

### Step 3 — Install Python Packages
Open your terminal (Command Prompt / Terminal) and run:
```bash
pip install flask flask-cors anthropic python-dotenv
```

### Step 4 — Add New Files to Your Project
Copy these files into your portfolio folder (same place as your old index.html):
- `index.html`       → replace your old index.html
- `ai-features.css`  → new file
- `ai-features.js`   → new file
- `app.py`           → new file
- `.env`             → new file (keep this SECRET, don't share it)

Your folder structure should look like:
```
portfolio/
├── index.html         ← updated
├── new1.css           ← unchanged
├── new1Media.css      ← unchanged
├── new1.js            ← unchanged
├── ai-features.css    ← NEW
├── ai-features.js     ← NEW
├── app.py             ← NEW
├── requirements.txt   ← NEW
├── .env               ← NEW (secret!)
└── assets/
    └── ...
```

### Step 5 — Run the Python Backend
In your terminal, navigate to your portfolio folder and run:
```bash
python app.py
```
You should see:
```
🚀 Starting Aman's Portfolio AI Backend...
📡 Running on http://localhost:5000
```

### Step 6 — Open Your Portfolio
Open `index.html` in your browser (or use Live Server in VS Code).

---

## 🎯 What You'll See

### AI Chatbot
- A floating **💬 button** appears at the bottom-right of your portfolio
- Click it to open the chat window
- Visitors can ask: "What are Aman's skills?", "Tell me about his projects", etc.
- The AI knows all about you from the context in app.py

### Project Summarizer
- Each project card now has a **✨ Ask AI** button
- Click it to generate an AI summary of that project
- Click again to hide the summary

---

## ⚠️ Important Notes

1. **Both must run at the same time**: Your HTML in browser + Python backend
2. **Never share your .env file** or commit it to GitHub
3. **Add .env to .gitignore** if using Git:
   ```
   echo ".env" >> .gitignore
   ```

---

## 🚀 Deploying Online (Later)

When you're ready to put this live:
- Deploy `app.py` to **Railway.app** or **Render.com** (both free)
- Update `API_BASE` in `ai-features.js` from `http://localhost:5000` to your deployed URL

---

## 🐛 Troubleshooting

| Problem | Solution |
|---|---|
| "Can't connect to AI" | Make sure `python app.py` is running |
| "Invalid API key" | Check your `.env` file has the correct key |
| Chat shows no response | Open browser DevTools → Console for errors |
| CORS error | Make sure `flask-cors` is installed |
