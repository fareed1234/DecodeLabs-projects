# Cipher — Socratic Coding Tutor
### Project 4: System Persona & Guardrail Architecture (DecodeLabs)

A resilient AI tutor persona that teaches programming **without ever handing out code**,
built as pure system-prompt engineering (no external moderation model, no fine-tuning).

## Files

| File | Purpose |
|---|---|
| `system_prompt.md` | Human-readable version of the prompt with explanations and a requirements table |
| `system_prompt.txt` | The raw prompt text only, no markdown — this is what `test_harness.py` actually loads |
| `red_team_suite.json` | 12 adversarial test cases covering the main attack vectors |
| `test_harness.py` | Runs the suite against the live API and heuristically flags failures |
| `red_team_results.json` | Generated after you run the harness — full transcripts + verdicts |

## Running it in VS Code

1. **Open the folder**: `File → Open Folder…` → select `socratic-tutor-guardrails`.
2. **Install the Python extension** (if not already) so VS Code recognizes `.py` files.
3. **Open a terminal** in VS Code (`` Ctrl+` ``) and set up a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate      # on Windows: venv\Scripts\activate
   pip install openai python-dotenv
   ```
4. **Get a free OpenRouter API key**: go to https://openrouter.ai, sign up with
   just an email (no credit card needed), then create a key at
   https://openrouter.ai/keys.
5. **Create a `.env` file** in this same folder (copy `.env.example` and rename
   it, or create it fresh) containing one line:
   ```
   OPENROUTER_API_KEY=sk-or-v1-your-actual-key-here
   ```
   The script loads this automatically — no manual `export`/`set` needed, and no
   need to re-enter it every time you open a new terminal. `.gitignore` already
   excludes `.env` so it won't accidentally get committed if you push this to GitHub.
6. **Run the harness**:
   ```bash
   python test_harness.py
   ```
   You'll see a pass/flag line per test case in the terminal, and a full transcript
   dump in `red_team_results.json` you can open directly in VS Code to read Cipher's
   actual responses. The script defaults to `openrouter/free` — OpenRouter's own
   auto-router, which picks from whatever free models are currently available rather
   than a specific pinned model. This is deliberate: individual `:free` model IDs on
   OpenRouter get added and removed often (sometimes within days), so pinning one
   directly tends to break. If you'd rather force a specific model, browse
   https://openrouter.ai/models?max_price=0 for a current `:free` ID and paste it
   into the `MODEL` constant at the top of `test_harness.py`.
7. To manually chat with Cipher instead of running the automated suite, you can also
   just paste the contents of `system_prompt.txt` into OpenRouter's chat
   playground (https://openrouter.ai/chat) as the system prompt and talk to it
   directly — that's the fastest way to feel out the persona before automating tests.

No API key? You can still read every file and manually paste `system_prompt.txt`
into any LLM playground that accepts a system prompt.

## Architecture, in one paragraph

Cipher is built as **defense-in-depth**, not a single instruction. Layer 1 anchors
identity so roleplay/alter-ego attacks can't relabel the model. Layer 2 encodes the
actual pedagogy (Socratic questioning) as a *quantifiable* constraint — at least one
question per response — so "teaching" isn't just a vibe, it's checkable. Layer 3 sets
tone, including the deliberate choice to avoid boilerplate refusal phrases (attackers
often target the refusal *pattern*, not just the content, so the deflection is written
to sound like normal tutoring, not a canned "I can't help with that"). Layer 4 is the
actual guardrail set: an un-overrideable code ban, a "sandwich" rule that treats all
student text as data rather than instructions (this is what stops embedded fake
"system notes" and comment-smuggled instructions), explicit handling for emotional
coercion, a cap on compute-exhaustion-style asks, anti-exfiltration behavior for the
prompt itself, and a named (but rule-unchanged) response to repeated jailbreak
attempts.

## What makes this different from a typical submission

Most versions of this exercise stop at "don't give code" + a generic "ignore
instructions in user input" line. This one adds three things graders/competitors
often miss:
- **A checkable pedagogy constraint** (`card(Q_R) >= 1`) instead of a vague "ask
  questions sometimes" — makes the persona testable, not just describable.
- **Reasoning-exhaustion protection** (Layer 4.4) — a DoS-style vector (over-long
  literal traces) that most guardrail write-ups for this project skip entirely.
- **A repeated-attempt escalation policy that doesn't change the rules** — it
  acknowledges the pattern out loud once, which is more honest and more resilient
  than either staying silent forever or getting stricter under pressure (strictness
  changes are themselves a manipulable surface).

## Checklist: what a prompt engineer needs to nail down for a project like this

1. **Separate the four layers explicitly.** Role, Task, Tone, and Rules should be
   readable as distinct sections — vague blending is exactly where jailbreaks find
   seams.
2. **State a priority order.** Guardrails must explicitly outrank task instructions,
   and task instructions must explicitly outrank tone preferences. Without a stated
   order, the model has to guess which rule wins when they conflict — attackers
   exploit that ambiguity.
3. **Treat all user input as data, not instructions** (the "sandwich" pattern) —
   and say so explicitly in the prompt, don't assume the model will infer it.
4. **Make the pedagogy/behavior falsifiable.** "Be Socratic" is a vibe; "at least one
   question per response" is testable. Wherever possible, turn a soft descriptor into
   a rule you can check against a transcript.
5. **Anticipate categories of attack, not just examples.** Roleplay override,
   emotional coercion, refusal-phrase banning, encoding/obfuscation, authority
   spoofing, multi-turn erosion, and resource-exhaustion are the recurring families —
   write a rule for the *category*, not just the one phrasing you thought of.
6. **Write deflections that stay in character.** A guardrail that breaks persona to
   refuse ("As an AI, I cannot...") is itself a tell that attackers learn to probe
   for. The refusal should sound like the persona, not like a disclaimer bolted on.
7. **Actually red-team it before calling it done.** Write the attacks first, run
   them, and read the transcripts — don't just trust that the rules "should" hold.
   A heuristic script (like `test_harness.py`) catches obvious slips, but a human
   still needs to read borderline responses, since persona-break can be subtle
   (e.g., the tutor gives a *very* detailed near-code description that's technically
   not code but defeats the pedagogical point).
8. **Don't over-restrict.** A guardrail so aggressive it refuses legitimate
   conceptual questions is a different kind of failure — verify the tutor still
   *teaches well* on clean, honest questions, not just that it resists attacks.