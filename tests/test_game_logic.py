from logic_utils import check_guess
from logic_utils import update_score
from logic_utils import get_range_for_difficulty

def test_winning_guess():
    outcome, message = check_guess(50, 50)
    assert outcome == "Win"

def test_guess_too_high():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"

def test_guess_too_low():
    outcome, message = check_guess(40, 50)
    assert outcome == "Too Low"

#BUG1 - PYTEST    
def test_score_on_first_attempt_win():
    # With attempts starting at 0, a win on attempt 1 (attempt_number=1)
    # should give 100 - 10*(1+1) = 80 points, not 70
    score = update_score(0, "Win", 1)
    assert score == 80

#BUG2 - PYTEST
def test_check_guess_too_high():
    outcome, message = check_guess(60, 50)
    assert outcome == "Too High"
    assert "LOWER" in message  # not HIGHER

def test_check_guess_too_low():
    outcome, message = check_guess(30, 50)
    assert outcome == "Too Low"
    assert "HIGHER" in message


#BUG3 - PYTEST
def test_new_game_respects_hard_difficulty():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 50  # not 100

def test_new_game_respects_easy_difficulty():
    low, high = get_range_for_difficulty("Easy")
    assert high == 20


# RAG - PYTEST
from rag_utils import retrieve_tips

def test_retrieve_tips_first_guess():
    # On first attempt, should always retrieve the first_guess tip
    tips = retrieve_tips(attempt_number=1, attempts_left=7, distance=50, outcome="Too Low")
    tags = [t["tag"] for t in tips]
    assert "first_guess" in tags

def test_retrieve_tips_few_attempts_left():
    # With 2 or fewer attempts left, should retrieve few_attempts_left tip
    tips = retrieve_tips(attempt_number=6, attempts_left=2, distance=15, outcome="Too High")
    tags = [t["tag"] for t in tips]
    assert "few_attempts_left" in tags

def test_retrieve_tips_very_close():
    # Distance of 3 or less should retrieve very_close tip
    tips = retrieve_tips(attempt_number=3, attempts_left=5, distance=2, outcome="Too Low")
    tags = [t["tag"] for t in tips]
    assert "very_close" in tags

def test_retrieve_tips_far_off():
    # Distance greater than 20 should retrieve far_off tip
    tips = retrieve_tips(attempt_number=2, attempts_left=6, distance=45, outcome="Too High")
    tags = [t["tag"] for t in tips]
    assert "far_off" in tags

def test_retrieve_tips_returns_list():
    # Should always return a list even in edge cases
    tips = retrieve_tips(attempt_number=1, attempts_left=8, distance=None, outcome=None)
    assert isinstance(tips, list)

def test_retrieve_tips_max_three():
    # Should never return more than 3 tips
    tips = retrieve_tips(attempt_number=1, attempts_left=2, distance=2, outcome="Too Low")
    assert len(tips) <= 3

# RAG Enhancement tests
def test_retrieve_tips_hard_mode_first_guess():
    tips = retrieve_tips(attempt_number=1, attempts_left=4, distance=25, outcome="Too Low", difficulty="Hard")
    tags = [t["tag"] for t in tips]
    assert "hard_mode" in tags

def test_retrieve_tips_easy_mode_first_guess():
    tips = retrieve_tips(attempt_number=1, attempts_left=5, distance=10, outcome="Too High", difficulty="Easy")
    tags = [t["tag"] for t in tips]
    assert "easy_mode" in tags

def test_retrieve_tips_hard_low_attempts():
    tips = retrieve_tips(attempt_number=4, attempts_left=1, distance=5, outcome="Too Low", difficulty="Hard")
    tags = [t["tag"] for t in tips]
    assert "hard_low_attempts" in tags
    