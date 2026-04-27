import json
import os

def load_knowledge_base(path: str) -> list:
    """Load tips from a knowledge base JSON file."""
    try:
        with open(path, "r") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"[RAG] Warning: knowledge base not found at {path}")
        return []
    except json.JSONDecodeError as e:
        print(f"[RAG] Error parsing knowledge base: {e}")
        return []


def retrieve_tips(
    attempt_number: int,
    attempts_left: int,
    distance: int | None,
    outcome: str | None,
    difficulty: str = "Normal",
) -> list[dict]:
    """
    Retrieve relevant tips from both knowledge bases based on game state.

    Args:
        attempt_number: How many guesses have been made
        attempts_left: How many guesses remain
        distance: Absolute difference between guess and secret
        outcome: "Too High", "Too Low", or None
        difficulty: "Easy", "Normal", or "Hard"

    Returns:
        List of matching tip dicts (max 3)
    """
    # Load both knowledge bases
    general_tips = load_knowledge_base("knowledge_base.json")
    difficulty_tips = load_knowledge_base("difficulty_tips.json")
    
    matched = []

    # --- Difficulty-specific tips FIRST (higher priority) ---
    for entry in difficulty_tips:
        tag = entry["tag"]

        if tag == "easy_mode" and difficulty == "Easy" and attempt_number == 1:
            matched.append(entry)
        elif tag == "normal_mode" and difficulty == "Normal" and attempt_number == 1:
            matched.append(entry)
        elif tag == "hard_mode" and difficulty == "Hard" and attempt_number == 1:
            matched.append(entry)
        elif tag == "hard_low_attempts" and difficulty == "Hard" and attempts_left <= 2:
            matched.append(entry)
        elif tag == "easy_close" and difficulty == "Easy" and distance is not None and distance <= 3:
            matched.append(entry)

    # --- General tips SECOND ---
    for entry in general_tips:
        tag = entry["tag"]

        if tag == "first_guess" and attempt_number == 1:
            matched.append(entry)
        elif tag == "few_attempts_left" and attempts_left <= 2:
            matched.append(entry)
        elif distance is not None:
            if tag == "very_close" and distance <= 3:
                matched.append(entry)
            elif tag == "close" and 3 < distance <= 10:
                matched.append(entry)
            elif tag == "far_off" and distance > 20:
                matched.append(entry)
        if tag == "too_high" and outcome == "Too High":
            matched.append(entry)
        elif tag == "too_low" and outcome == "Too Low":
            matched.append(entry)

    # --- Difficulty-specific tips ---
    for entry in difficulty_tips:
        tag = entry["tag"]
        diff = entry.get("difficulty", "")

        if tag == "easy_mode" and difficulty == "Easy" and attempt_number == 1:
            matched.append(entry)
        elif tag == "normal_mode" and difficulty == "Normal" and attempt_number == 1:
            matched.append(entry)
        elif tag == "hard_mode" and difficulty == "Hard" and attempt_number == 1:
            matched.append(entry)
        elif tag == "hard_low_attempts" and difficulty == "Hard" and attempts_left <= 2:
            matched.append(entry)
        elif tag == "easy_close" and difficulty == "Easy" and distance is not None and distance <= 3:
            matched.append(entry)

    # Deduplicate and cap at 3 tips
    seen = set()
    unique = []
    for entry in matched:
        if entry["tag"] not in seen:
            seen.add(entry["tag"])
            unique.append(entry)

    print(f"[RAG] Retrieved {len(unique)} tips for state: attempt={attempt_number}, left={attempts_left}, distance={distance}, outcome={outcome}, difficulty={difficulty}")
    return unique[:3]


def build_coach_prompt(tips: list[dict], game_state: dict) -> str:
    """
    Build the prompt for the AI using retrieved tips and game state.
    This is the Augmentation step of RAG.
    """
    tip_text = "\n".join(f"- {t['tip']}" for t in tips)

    prompt = f"""You are a helpful game coach for a number guessing game.

Use ONLY the following retrieved strategy tips to guide your advice:
{tip_text}

Current game state:
- Difficulty: {game_state['difficulty']}
- Attempts used: {game_state['attempt_number']}
- Attempts remaining: {game_state['attempts_left']}
- Last outcome: {game_state['outcome']}

Give the player one short, encouraging coaching message (2-3 sentences max).
Do not reveal the secret number. Base your advice strictly on the tips above.
"""
    return prompt