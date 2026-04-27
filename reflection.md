# 💭 Reflection: Glitchy Guesser — Applied AI System

## 1. What are the limitations or biases in your system?

The biggest limitation is the knowledge base itself. It only contains 7 tips, all written from a single perspective — binary search strategy. This means the AI Coach will always nudge the player toward midpoint guessing, even if a different approach might work better for a specific player's style. The system has no way to learn from past games or adapt to how an individual player actually behaves.

There is also a retrieval bias built into the tag matching logic. The "first_guess" tip fires on every single first attempt regardless of context, which means a player who already knows binary search strategy will receive redundant advice on their opening guess every game. The retriever does not know anything about the player's skill level — it only knows the current game state.

Finally, the LLaMA model itself may have biases from its training data. Since the prompt is tightly constrained by retrieved tips, this risk is reduced — but the model still controls the tone and phrasing of every coaching message, and there is no guarantee it will always be encouraging rather than discouraging.

---

## 2. Could your AI be misused, and how would you prevent that?

The AI Coach in this game has a narrow scope, so direct misuse is limited. However, there are a few realistic risks worth noting.

The Groq API key, if exposed, could be used by others to make API calls at the key owner's expense. This is prevented by storing the key in a `.env` file that is excluded from GitHub via `.gitignore`, so the key is never committed to the repository.

The prompt sent to the model includes game state information like difficulty, attempts left, and outcome. If someone modified `rag_utils.py` to inject arbitrary text into the prompt, they could attempt a prompt injection attack — feeding the model instructions disguised as game context. This could be mitigated by sanitizing all inputs before they enter the prompt and by keeping the system prompt strict.

Finally, because the AI Coach speaks in an encouraging tone, a poorly designed version of this system could theoretically be used to keep players engaged beyond what is healthy — a dark pattern common in game design. The current implementation does not do this, but it is worth being aware of when building AI systems in consumer-facing games.

---

## 3. What surprised you while testing your AI's reliability?

Two things stood out.

First, the fallback behavior was more reliable than expected. When the Groq API failed due to an invalid key or a decommissioned model, the except block caught the error silently and displayed the raw tip text from the knowledge base instead. From the player's perspective, the game kept working — they still received a coaching message. This made the system feel more robust than it actually was under the hood, which was both reassuring and a little concerning.

Second, the model's output quality was surprisingly consistent given how small the retrieved context was. Passing in 2-3 short tip strings was enough for LLaMA 3.3 to generate a coherent, specific, encouraging coaching message every time. The tight prompt structure — telling the model to use only the retrieved tips and nothing else — was the key factor. Without that constraint, early testing showed the model would occasionally ignore the tips and give generic advice.

---

## 4. Describe your collaboration with AI during this project

**One instance where AI gave a helpful suggestion:**
When building the RAG pipeline, I asked Claude to explain how `attempt_number` fed into the `update_score` point calculation. Claude traced the full data flow and explained that because `attempts` was initialized to 1 instead of 0, the first guess was already being treated as attempt 2 in the scoring formula — giving fewer points than intended. This framing helped me understand that the bug was not just a display issue but had real downstream effects on scoring. That explanation led directly to the correct fix.

**One instance where AI gave a flawed or incomplete suggestion:**
When fixing Bug 2, I asked Copilot to remove the `TypeError` except block from `check_guess`. It did so correctly — but it did not catch that the root cause of the type mismatch was still in `app.py`, where `st.session_state.secret` was being cast to a string before being passed into the function. The AI fixed the symptom without identifying the cause. The game continued to crash on even-numbered attempts until I manually traced the data flow and removed the string cast in `app.py` myself. This was a clear reminder that AI suggestions need to be verified end-to-end, not just at the function level.