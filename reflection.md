# 💭 Reflection: Game Glitch Investigator

## 1. What was broken when you started?

1. Bug 1: Attempts counter started at 1 instead of 0. 

When I started the game, I expected the attempts counter should start at 0 so the first guess counts as attemp 1. 

However 'st.session_state.attempts' was initialized to 1, which meant the game started one attempt ahead and impacted the 'update_Score' function from the first guess, since 'attempt_number' went directly into the points formula.

2. Bug 2: 'check_guess' returned backwards direction hints

If my guess was too high - example 8-, but the secret is 50, the hint should say to 'GO LOWER' instead it said 'GO HIGHER.'
The hints were inverted and mislad the player (me) in the wrong direction. 

3. Bug 3: New game ignored the difficulty level and always picked from 1-100. 

When clicking 'New Game' on 'Hard' mode, it should've geenrated a secret number within 1-50. 

However, the 'new_game' block hardcoded 'random.randint(1-100) instead of calling 'get_range_for_difficulty(difficulty), so the difficulty setting was ignored on reset. 


## 2. How did you use AI as a teammate?

I asked Claude AI to move check_guess from app.py into logic_utils.py to fix the inverted hint messages and remove 'TypeError' except block.
Claude was able to:
-  replaced the 'NotImplementedError' stub in 'logic_tils.py' with the real implementation.
- fix the guess>secret to return 'GO LOWER' instead of 'GO HIGHER'
- Add the import 'from logic_utils import check _guess' to 'app.py'
- remove the original duplicate lines - 17-line 'check_Guess' definition from 'app.py'

I verified this by running 'pytest' and by manually testing in the live Streamlit app. A high number now correctly showed 'GO LOWER'.


An AI suggestion that was incorrect/misleading was - removing the 'TypeError' block without fixing the root cause. 
What happened here is that I asked Copilot to remove the 'TypeError' except block from 'check_guess,' it did so correctly, but it didn't catch that the root cause of the mismatch was still in 'app.py'. 
When I was playing the game and entering guesses like 97 and 99, it triggered the crash. This was fixed and verified by removing str/int cast entirely and always passing the integer secret. 


## 3. Debugging and testing your fixes

- How did you decide whether a bug was really fixed?

I used a two-step check for each bug. First I ran pytest to confirm the automated test passed — this told me the logic function itself was behaving correctly in isolation. Then I ran the live Streamlit app and manually triggered the exact scenario that caused the original bug. A passing test alone wasn't enough, because Bug 2 showed that the logic in logic_utils.py could be correct while the code in app.py was still broken. Both layers had to work together before I considered a bug truly fixed.

- Describe at least one test you ran (manual or using pytest) and what it showed you about your code.

The most revealing test was test_check_guess_too_high() for Bug 2. Before the fix, this test would have passed the outcome assert but failed on "LOWER" because the message was returning "Go HIGHER" instead. After fixing the hint messages in logic_utils.py, the test passed — but the game still crashed on even-numbered attempts with a TypeError. That told me the function itself was correct but something upstream in app.py was passing the wrong type into it. The test isolated exactly where the problem wasn't, which pointed me to where it actually was — the str cast on st.session_state.secret.

- Did AI help you design or understand any tests? How?

Yes.I asked Claude AI to suggest a pytest case for each bug fix, and it gave me a useful starting structure. For Bug 1, it explained that the best way to test the attempts initialization was to call update_score directly with attempt_number=1 and assert the expected point value, since that's where the off-by-one error had downstream impact. That framing — testing the consequence of the bug, not just the line that changed — helped me write more meaningful tests than simply checking attempts == 0. However, Copilot did not suggest testing the str/int crash scenario for Bug 2, which I had to identify and verify manually by playing the game.

## 4. What did you learn about Streamlit and state?

- How would you explain Streamlit "reruns" and session state to a friend who has never used Streamlit?

Every time you click a button or type something, Streamlit reruns the entire script from the top. Without st.session_state, everything resets — your score, your guesses, the secret number. Session state is a notebook that survives reruns, so the game remembers where you left off. The not in st.session_state guard is how you say "only set this on the very first run, leave it alone after that." Bug 1 was a direct result of getting this wrong — initializing attempts to 1 every time instead of just once.

## 5. Looking ahead: your developer habits

- What is one habit or strategy from this project that you want to reuse in future labs or projects?
  - This could be a testing habit, a prompting strategy, or a way you used Git.

Starting a fresh Copilot Chat session for each individual bug. Keeping the AI focused on one problem at a time produced much cleaner suggestions than mixing multiple bugs into one conversation. Combined with using #file: context variables to point Copilot at the exact files involved, this made the AI's responses specific and actionable rather than generic. I'll carry this "one session per problem" approach into any future project where I'm using AI assistance.
 
- What is one thing you would do differently next time you work with AI on a coding task?

Before asking the AI to fix anything, I would first ask it to trace the full data flow of the bug — from where the value originates to where it's used. For Bug 2, asking "how does secret travel from st.session_state into check_guess?" before requesting a fix would have caught the str cast in app.py upfront, instead of discovering it as a crash after the fact. Understanding first, fixing second.

- In one or two sentences, describe how this project changed the way you think about AI generated code.

I came in assuming that if the AI's code looked clean and ran without immediate errors, it was probably correct — this project proved that wrong. AI can produce confident, well-formatted code that fixes the symptom while leaving the root cause completely untouched, and the only way to catch that is to read carefully, test deliberately, and never skip the step of running it yourself.