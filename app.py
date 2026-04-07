from flask import Flask, request, jsonify
from flask_cors import CORS
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# ── Configure Groq ────────────────────────────────────────────────────────────
client = Groq(api_key=os.getenv("GROQ_API_KEY"))
MODEL = "llama-3.3-70b-versatile"  # Free, fast, capable model

# ── Portfolio context so AI knows about Aman ──────────────────────────────────
PORTFOLIO_CONTEXT = """
You are a helpful AI assistant on Aman's personal portfolio website.
Here is everything you know about Aman:

NAME: Aman
COLLEGE: IIT Indore (Indian Institute of Technology Indore)
DEGREE: B.Tech in Electrical Engineering
HOMETOWN: Panchkula, Haryana
EXPERIENCE: 1+ year in Software Development

SKILLS:
- Programming: Java, JavaScript, Python, HTML, CSS
- Frameworks: React JS
- Database: MySQL
- Tools: Git, GitHub, AI/ML

PROJECTS:
1. SoulWisdom
   - A web application
   - React, Tailwind CSS
   - Built a responsive web app providing mental wellness resources and personalized support.
   - Designed an intuitive UI with React to enhance user engagement.
   - Utilized Tailwind CSS for fast and easy styling with a responsive design.
   - Deployed the app for real-time use and feedback.
   - GitHub: https://github.com/amanmr795/SoulWisdom.git
   - Live Demo: https://soul-wisdom.vercel.app/

2. PS Automation
   -  Complete Project name : Grey-box Approach for Modeling of Converter Interfaced Power Systems
   -  Work under Dr. Lokesh Kumar Dewangan
   -  Grey-Box Power System Modeling: Created a validated grey-box model of a power converter by combining simu
lation results (Python/PSCAD) with a mathematical model (MATLAB).
   - Automated Frequency Analysis: Built a Python framework to automate PSCAD simulations, determining the
converter’s admittance matrix by injecting small-signal voltage perturbations and measuring the resulting current
response.
   - Data Processing & Visualization: Processed simulation data using Python (NumPy, Matplotlib) and FFTs to
generate frequency-domain models and Bode plots for analysis.
   - System Stability Assessment: Used the validated model to analyze power system stability with Nyquist criteria
and Eigenvalue decomposition
   - GitHub: https://github.com/amanmr795/Grey-box-Approach-for-Modeling-of-Converter-Interfaced-Power-Systems.git

SOCIAL & CONTACT:
- Email: amanmr795@gmail.com
- LinkedIn: https://www.linkedin.com/in/amaniitindore795/
- GitHub: https://github.com/amanmr795
- Codolio: https://codolio.com/profile/aman_iiti/

PERSONALITY: Passionate about coding, curious learner who started coding while doing Electrical Engineering.
Believes coding has been an "absolute revelation" in his journey.

INSTRUCTIONS:
- Answer questions about Aman warmly and professionally.
- If asked something you don't know, say "I don't have that info, but you can reach Aman at amanmr795@gmail.com"
- Keep responses concise (2-4 sentences max unless asked for more).
- Be friendly and encouraging about Aman's work.
- Do NOT make up information that is not provided above.
"""


# ── Route 1: AI Chatbot ───────────────────────────────────────────────────────
@app.route("/api/chat", methods=["POST"])
def chat():
    try:
        data = request.get_json()
        user_message = data.get("message", "").strip()

        if not user_message:
            return jsonify({"error": "No message provided"}), 400

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": PORTFOLIO_CONTEXT},
                {"role": "user",   "content": user_message}
            ],
            max_tokens=512,
            temperature=0.7
        )

        reply = response.choices[0].message.content
        return jsonify({"reply": reply})

    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({"error": "Something went wrong. Please try again."}), 500


# ── Route 2: Project Summarizer ───────────────────────────────────────────────
@app.route("/api/summarize-project", methods=["POST"])
def summarize_project():
    try:
        data = request.get_json()
        project_name        = data.get("name", "")
        project_description = data.get("description", "")
        github_url          = data.get("github", "")
        demo_url            = data.get("demo", "")

        prompt = f"""
        You are summarizing a software project for a portfolio website.
        Generate an engaging 3-sentence summary for this project:

        Project Name: {project_name}
        Description/Context: {project_description}
        GitHub: {github_url}
        Demo: {demo_url if demo_url else "Not available"}

        The summary should:
        - Explain what the project does in plain English
        - Highlight what makes it interesting or technically impressive
        - Be written in an excited, professional tone
        - Be exactly 3 sentences
        """

        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "user", "content": prompt}
            ],
            max_tokens=256,
            temperature=0.7
        )

        summary = response.choices[0].message.content
        return jsonify({"summary": summary})

    except Exception as e:
        print(f"Summarize error: {e}")
        return jsonify({"error": "Could not generate summary. Please try again."}), 500


# ── Health check ──────────────────────────────────────────────────────────────
@app.route("/api/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "message": "Aman's AI backend is running with Groq!"})

@app.route("/")
def home():
    return "Aman's AI Backend is running 🚀"

if __name__ == "__main__":
    print("🚀 Starting Aman's Portfolio AI Backend (Groq)...")
    print("📡 Running on http://localhost:5000")
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)