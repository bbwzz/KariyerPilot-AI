# 🚀 KariyerPilot AI

**A Composite AI Career Recommendation & Technical Roadmap Engine**

KariyerPilot AI is an intelligent profiling tool designed to help developers and students bridge the gap between their current technical skill sets and their target career paths. By combining traditional data-processing algorithms with Google's state-of-the-art Generative AI, it computes market compatibility and synthesizes highly personalized, week-by-week study blueprints.

---

## ✨ Key Features

* **📊 Predictive Profiling & Analytics:** Evaluates current technical tools against industry standards to assign predictive cohort personas and compute percentage-based match scores for various tech tracks.
* **🎯 Intelligent Gap Analysis:** Automatically isolates missing fundamental skills required for a selected career target.
* **⚡ Generative Blueprinting:** Leverages Google's Gemini Flash model to synthesize actionable 4-week study plans focused explicitly on closing identified skill gaps.
* **🛠️ Capstone Project Generation:** Recommends custom portfolio projects that merge the user's existing toolset with their newly acquired target skills.

---

## 🏗️ Architecture: The Composite AI Approach

This project utilizes a **Composite AI** design pattern, cleanly separating deterministic data processing from generative reasoning:
1.  **The Backend (`backend.py`):** Handles deterministic logic, local skill scoring, gap detection, and market compatibility clustering. 
2.  **The Agent (`ai_agent.py`):** Handles generative synthesis using the `google-genai` SDK, taking the rigid data from the backend and expanding it into natural language study structures.
3.  **The Interface (`app.py`):** Orchestrates the data flow and presents a clean, responsive single-page dashboard using Streamlit.

---

## ⚙️ Local Setup & Installation

### 1. Clone the Repository

git clone [https://github.com/your-username/KariyerPilot-AI.git](https://github.com/your-username/KariyerPilot-AI.git)
cd KariyerPilot-AI
2. Install Dependencies
Ensure you have Python 3.9+ installed, then run:

Bash
pip install streamlit scikit-learn pandas google-genai pydantic python-dotenv
3. Environment Configuration
You need an active Google Gemini API Key to power the generative agent layer.

Get a free API key from Google AI Studio.

Create a file named exactly .env in the root directory.

Add your key to the file (no spaces, no quotes):

Plaintext
GEMINI_API_KEY=AIzaSyYourActualKeyHere
4. Launch the Application
Bash
streamlit run app.py
The application will automatically open in your default browser at http://localhost:8501.
```text
📂 Project Structure
Plaintext
KariyerPilot-AI/
├── .env                # Ignored by git: Securely stores API keys
├── .gitignore          # Keeps environment files and IDE caches out of version control
├── README.md           # Project documentation
├── ai_agent.py         # Google GenAI connection layer and Pydantic schemas
├── app.py              # Main Streamlit application and UI layout
└── backend.py          # Math, data schemas, and analytics engine
```
Built with Python, Streamlit, and Google Gemini.
