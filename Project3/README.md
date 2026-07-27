# Project 3: Context-Anchored Answering (RAG Basics)

**Prompt Engineering — Industrial Training Kit | DecodeLabs | Batch 2026**

## Overview

This project implements a **closed-book, context-locked prompting system** that prevents LLM hallucination by:

1. Restricting the model to answer *only* from injected reference text
2. Enforcing a strict negative constraint (`"Information Not Found"`) when the answer isn't present
3. Requiring exact paragraph-level citations (`[Para X]`) for every claim

## Repo Structure

```
project3-rag-basics/
├── README.md                  # This file
├── prompts/
│   └── system_prompt.md       # The core reusable prompt template
├── tests/
│   └── test_cases.md          # Test cases proving robustness (valid, trick, distractor, injection)
└── docs/
    └── requirements_mapping.md # Maps each project requirement to its implementation
```

## Key Skills Demonstrated

- Context injection
- Retrieval-Augmented Generation (RAG) principles
- Negative constraints / deflection protocols
- Source attribution & factuality enforcement
- Prompt-injection resistance

## Quick Start

1. Copy the template from `prompts/system_prompt.md`
2. Replace `{INSERT_REFERENCE_DOCUMENT_HERE}` with your source text (paragraph-numbered)
3. Replace `{INSERT_USER_QUESTION_HERE}` with the user query
4. Run it against your LLM of choice and validate against `tests/test_cases.md`

## Author

Muhammad Fareed — BS Computer Science (HCI Track), UMT Lahore
