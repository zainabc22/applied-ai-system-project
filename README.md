# 🎮 Glitchy Guesser — Applied AI System

## 📌 Original Project Summary

This project is an extension of **Game Glitch Investigator** (Module 1), a Streamlit-based number guessing game that was intentionally shipped with three bugs. The original project tasked students with finding and fixing broken game logic — including an inverted hints system, an off-by-one attempts counter, and a difficulty setting that was ignored on new game resets. All three bugs were identified, fixed, and verified using AI-assisted debugging and pytest.

---

## 🧠 What This System Does

Glitchy Guesser is a number guessing game with an **AI-powered coaching system** built on Retrieval-Augmented Generation (RAG). After every guess, the game retrieves relevant strategy tips from a local knowledge base, builds a context-aware prompt using the current game state, and sends it to a language model (Groq/LLaMA) to generate a personalized coaching message for the player.

The AI Coach actively changes what the system says based on what was retrieved — it is not a static response. A player who is far off on their first guess gets different advice than a player with 2 attempts left who is within 3 numbers of the secret.

---

## 🗂️ Project Structure

```
applied-ai-system-project/
├── assets/                  # System architecture diagram
├── tests/
│   └── test_game_logic.py   # 17 pytest tests covering game logic and RAG
├── app.py                   # Main Streamlit app
├── logic_utils.py           # Game logic: check_guess, update_score, get_range_for_difficulty
├── rag_utils.py             # RAG pipeline: retrieve_tips, build_coach_prompt
├── knowledge_base.json      # Local tip database (7 tagged strategy tips)
├── difficulty_tips.json     # Difficulty-specific tip database
├── requirements.txt         # Dependencies
├── .env                     # API key (not committed to GitHub)
├── .gitignore
└── README.md
```

---

## 🏗️ Architecture Overview

The system has four layers:

**UI Layer** (`app.py`) — Streamlit handles session state, user input, and display. Every guess triggers both the game logic and the RAG pipeline.

**Game Logic Layer** (`logic_utils.py`) — Pure Python functions handle guess checking, score updates, and difficulty ranges. These are fully tested and independent of the UI.

**RAG Layer** (`rag_utils.py` + `knowledge_base.json`) — On each guess, the retriever selects 1-3 relevant tips from the knowledge base based on game state (attempt number, distance from secret, outcome). These tips are injected into a prompt alongside the current game context.

**AI Generation Layer** (Groq API / LLaMA 3.3) — The augmented prompt is sent to the model, which generates a personalized 2-3 sentence coaching message grounded in the retrieved tips.

![System Architecture](assets/system_architecture.png)

---

## ⚙️ Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/your-username/applied-ai-system-project.git
cd applied-ai-system-project
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

On Windows if pip is unavailable:
```powershell
py -m pip install -r requirements.txt
```

### 3. Set up your API key

Create a `.env` file in the project root:
```
GROQ_API_KEY=your_groq_api_key_here
```

Get a free API key at https://console.groq.com

### 4. Run the app
```bash
python -m streamlit run app.py
```

On Windows:
```powershell
py -m streamlit run app.py
```

### 5. Run the tests
```bash
pytest tests/test_game_logic.py -v
```

---

## 💬 Sample Interactions

**Example 1 — First guess, far off:**
> Player guesses 17, secret is 68.
> Hint: Go HIGHER!
> AI Coach: You are off to a great start — with 7 attempts remaining, make a bold jump toward the center of the remaining range to eliminate as many possibilities as possible.

**Example 2 — Getting close, few attempts left:**
> Player guesses 65, secret is 68.
> Hint: Go HIGHER!
> AI Coach: You are almost there! With only 2 attempts left, focus on splitting the remaining gap in half — the secret is just above your last guess.

**Example 3 — Too high, mid-game:**
> Player guesses 80, secret is 68.
> Hint: Go LOWER!
> AI Coach: Good progress — your guess was too high, so cut the upper half of your range. The secret is below 80, try picking the midpoint of what is left.

---

## 🧩 Design Decisions

**Why RAG instead of a static hint system?**
A static hint system would always say the same thing. RAG lets the coaching message adapt to the exact game state — how many attempts are left, how far off the guess was, and which direction to go. The retrieval step is what makes the advice specific rather than generic.

**Why a local JSON knowledge base?**
For a game of this scope, a local JSON file is the right tool. It is fast, transparent, easy to edit, and does not require a vector database or embedding model. The tags make retrieval logic simple and auditable.

**Why Groq / LLaMA instead of a larger model?**
Groq's free tier is fast and sufficient for 2-3 sentence coaching messages. The prompt is tightly constrained by retrieved tips, so a smaller model performs well without needing a larger model's capability.

**Why keep logic functions in logic_utils.py?**
Separating logic from the UI makes testing easier and keeps app.py focused on display. Any function that can be unit tested belongs in logic_utils.py.

---

## 🧪 Testing Summary

17 pytest tests covering all core logic and the RAG pipeline. All 14 pass.

| Category | Tests | Result |
|---|---|---|
| Game logic (check_guess) | 4 | Pass |
| Difficulty ranges | 2 | Pass |
| Score calculation | 1 | Pass |
| RAG retrieval | 6 | Pass |
| RAG Enhancement (difficulty tips) | 3 | Pass |
| Edge cases | 1 | Pass |

**What the tests proved:**
- check_guess correctly returns "Too High" with a "Go LOWER" message and vice versa
- retrieve_tips returns the right tip tags for first guess, close range, far off, and low attempts scenarios
- Tips are always capped at 3 and always return a list even for edge case inputs
- Hard mode correctly uses range 1-50, not 1-100

**What was tested manually:**
- The Groq API call (verified by playing the game and observing AI Coach output)
- The full prompt output of build_coach_prompt (verified via terminal logs)

---

## 🪞 Reflection

This project extended a simple bug-fixing exercise into a working applied AI system. The most important lesson was that RAG is not just about calling an API — the retrieval step is what makes the generation trustworthy. Without retrieved tips constraining the prompt, the model could say anything. With them, every coaching message is grounded in specific, relevant strategy.

The biggest challenge was the Python environment setup on Windows (msys64 vs python.org). Once the correct Python installation was used, the rest of the pipeline came together quickly.

If extending this further, the next step would be a RAG Enhancement: replacing the JSON knowledge base with a document store of full strategy guides, so the retriever can pull paragraph-level context rather than single tips.

---

## 📸 Demo

![Winning game screenshot](image.png)

![AI Coach in action](assets/game_demo.png)

