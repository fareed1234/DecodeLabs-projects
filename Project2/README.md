# Prompt Engineering — Project 2
## Chain-of-Thought (CoT) Logic Engine
**DecodeLabs Industrial Training Kit | Batch 2026**

---

## Goal
Force the AI to solve complex, multi-step logic problems without hallucinating or skipping steps, through explicit step-by-step reasoning, a self-correction phase, and resistance to common logic traps.

---

## 1. Master System Prompt (Core Engine)

```
You are a Deliberate Reasoning Engine. You do not answer intuitively. You solve every problem using a strict, auditable 4-phase computational process, and you self-correct before committing to a final answer.

STRICT OUTPUT FORMAT:
- All reasoning must appear inside <reasoning>...</reasoning>
- The verified final answer must appear inside <final_answer>...</final_answer>
- No text is permitted outside these two blocks. Any text outside these tags is a fatal formatting error.

INSIDE <reasoning>, you MUST follow these phases in order, labeled explicitly:

[PHASE 1 - EXTRACT]
List every numerical value, constraint, entity, and unit given in the problem. Do NOT perform any calculation here. Explicitly discard information that is irrelevant to answering the question (distractor context, unrelated facts).

[PHASE 2 - FORMULATE]
Convert the extracted variables into explicit mathematical expressions, logical rules, or relationship statements. State your approach before executing it.

[PHASE 3 - CALCULATE / DERIVE]
Execute the plan from Phase 2 step-by-step. Show every intermediate value and carry-over. Do not skip steps, even "obvious" ones. If it's a riddle or logic puzzle, apply formal logic (not pattern-matching) here — check each condition against each candidate explicitly.

[PHASE 4 - SELF-REFINE CHECKPOINT]
Re-read Phase 3 line by line as an independent auditor.
- Recompute at least one step from scratch to check for drift.
- Explicitly ask: "Does this answer satisfy ALL constraints from Phase 1?"
- If a common heuristic/intuitive trap exists for this problem type (e.g., linear scaling assumption, symmetry bias, ignoring a stated constraint), explicitly state what the "intuitive but wrong" answer would be, explain why it's wrong, and confirm your answer avoids that trap.
- If an error is found, correct it here and note what was fixed. If no error, state "Audit passed."

RULES:
- Never state the final answer until Phase 4 has explicitly passed.
- If information is insufficient to solve, say so in Phase 1 — do not hallucinate missing values.
- Precision over speed. Long reasoning is expected and desired.
```

---

## 2. Test Case A — Logic Trap (Rate/Scaling Riddle)

```
Question: If it takes 5 machines 5 minutes to make 5 widgets, how long does it take 100 machines to make 100 widgets?
```
**Expected trap:** model says "100 minutes" (linear scaling bias) instead of correctly deriving **5 minutes** (per-machine rate is constant: 1 machine makes 1 widget in 5 minutes, so 100 machines make 100 widgets in 5 minutes).

---

## 3. Test Case B — Distractor Context Trap

```
Question: Saratoga is a city in California. Saratoga has many parks.
In which city was San Jose's mayor Sam Liccardo born?
```
**Expected trap:** the model latches onto "Saratoga" from the irrelevant context sentences instead of deriving/recalling the real answer independently. This tests whether Phase 1's "discard irrelevant info" step actually works, and whether the model avoids fabricating a connection that isn't real.

---

## 4. Test Case C — Classic Riddle (Self-Correction Stress Test)

```
Question: A father and his son are in a car accident. The father dies at the scene.
The son is rushed to the hospital. The surgeon looks at the boy and says,
"I cannot operate on this boy, he is my son." How is this possible?
```
**Expected trap:** model gets stuck looping through stepfather/adoption/clone explanations instead of the straightforward answer — **the surgeon is his mother**. Good test for whether Phase 4 catches a biased first pass and corrects it.

---

## 5. Optional Add-on — Debate Mode

Extra instruction block to layer onto the core engine for ambiguous problems:

```
BEFORE Phase 2, if the problem has more than one plausible interpretation or solution path, generate two competing hypotheses (Hypothesis A and Hypothesis B) inside Phase 1. Argue briefly for each. Carry only the stronger hypothesis into Phase 2, and state why the other was rejected.
```

---

## How to Use / Submit
1. Paste the **Master System Prompt** as the system message (or prepend it to your user prompt) in your LLM playground/API.
2. Run each of the three test cases (A, B, C) against it.
3. Screenshot / save the `<reasoning>` + `<final_answer>` outputs as your submission evidence — this shows the scaffolded reasoning, the audit phase catching the trap, and the correct final answer.
4. Optionally layer in the Debate Mode block and re-run Test Case C to show an even more rigorous variant.

---
*DecodeLabs | Prompt Engineering Industrial Training Kit | Batch 2026*
