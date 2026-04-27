# 🃏 Model Card: Glitchy Guesser AI Coach

## Model Overview

| Field | Details |
|---|---|
| Model Name | LLaMA 3.3 70B Versatile |
| Provider | Groq API |
| Version | llama-3.3-70b-versatile |
| Task | Conversational coaching / strategy generation |
| Integration | Retrieval-Augmented Generation (RAG) |
| Application | Glitchy Guesser — Number Guessing Game AI Coach |

---

## What the Model Does

The model generates personalized 2-3 sentence coaching messages for players of the Glitchy Guesser number guessing game. It does not operate freely — every response is grounded by retrieved strategy tips from a local knowledge base. The model's role is to take those tips and the current game state and produce a natural, encouraging message tailored to the player's exact situation.

The model never sees the secret number and cannot reveal it. Its output is constrained by the prompt structure, which instructs it to base advice strictly on the retrieved tips.

---

## How It Is Used

### RAG Pipeline

1. After each guess, `rag_utils.py` retrieves 1-3 relevant tips from two knowledge bases based on game state (attempt number, distance from secret, outcome, difficulty level)
2. Retrieved tips are injected into a structured prompt alongside current game context
3. The prompt is sent to LLaMA 3.3 via the Groq API
4. The model generates a coaching message grounded in the retrieved tips
5. If the API call fails, the system falls back to displaying the raw tip text directly

### Example Prompt Structure

```
You are a helpful game coach for a number guessing game.

Use ONLY the following retrieved strategy tips to guide your advice:
- Hard mode gives you only 5 attempts for 1-50 — every guess must cut the range in half.
- You are running low on attempts — calculate the exact midpoint of what remains.

Current game state:
- Difficulty: Hard
- Attempts used: 4
- Attempts remaining: 1
- Last outcome: Too Low

Give the player one short, encouraging coaching message (2-3 sentences max).
Do not reveal the secret number. Base your advice strictly on the tips above.
```

---

## Intended Use

- Providing real-time strategy coaching in a number guessing game
- Demonstrating how RAG constrains and grounds AI-generated responses
- Educational demonstration of responsible AI system design

## Out of Scope Use

- This model should not be used to make decisions outside the game context
- The coaching system is not designed for competitive or high-stakes environments
- The system should not be extended to collect or store player data without appropriate consent

---

## Limitations and Biases

**Knowledge base bias:** All tips are written from a binary search perspective. Players who prefer other strategies will always receive midpoint-focused advice regardless of their approach.

**Skill level blindness:** The retriever has no knowledge of the player's skill level. A beginner and an expert receive coaching based only on the current game state, not their history or experience.

**Language:** All tips and generated responses are in English only. The system has no multilingual support.

**Model hallucination risk:** Although the prompt instructs the model to use only retrieved tips, LLMs can occasionally ignore instructions and generate advice not grounded in the knowledge base. The tight prompt structure reduces but does not eliminate this risk.

**API dependency:** The full AI coaching feature requires an active Groq API key and internet connection. Without these, the system falls back to raw tip text, which is functional but less personalized.

---

## Reliability and Testing

| Test Type | Coverage | Result |
|---|---|---|
| Unit tests (game logic) | check_guess, update_score, difficulty ranges | 14/14 pass |
| RAG retrieval tests | retrieve_tips across all game states | 6/6 pass |
| RAG Enhancement tests | difficulty-specific tip retrieval | 3/3 pass |
| Manual testing | Groq API output, fallback behavior, difficulty switching | Verified |

**Total: 17/17 automated tests passing**

**Fallback behavior verified:** When the API key is missing or invalid, the except block catches the error silently and displays the raw tip text. The game remains fully playable without the AI generation layer.

**Logging:** Every retrieval is logged to the terminal with attempt number, attempts left, distance, outcome, and difficulty — making it easy to audit what the system retrieved and why.

---

## AI Collaboration Notes

**Helpful AI suggestion:** Claude traced the full data flow of the `attempt_number` variable and explained how initializing `st.session_state.attempts` to 1 instead of 0 caused downstream scoring errors. This framing — following the variable from initialization through the scoring formula — was more useful than just being told to change a number.

**Flawed AI suggestion:** When asked to fix the `TypeError` in `check_guess`, Copilot removed the except block correctly but did not identify that the root cause was a string cast on `st.session_state.secret` in `app.py`. The function-level fix was correct but incomplete — the crash persisted until the upstream cast was manually identified and removed.

---

## Responsible Design Notes

- The API key is stored in a `.env` file excluded from version control via `.gitignore`
- The model is never given the secret number, preventing it from leaking game information
- Error handling ensures the app never crashes due to API failure
- The system prompt explicitly constrains the model to use only retrieved tips, reducing the risk of off-topic or harmful outputs
- No player data is stored or transmitted beyond what is needed for a single API call