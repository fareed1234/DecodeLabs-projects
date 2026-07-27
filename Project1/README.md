# Project 1 — Zero-Shot & Few-Shot Data Extraction

A deterministic JSON extraction engine built with a strict-delimiter, few-shot
prompt and `temperature=0`, using the Gemini API. Takes a messy customer
support email and extracts 5 fields into a locked JSON schema, returning
`null` for anything missing instead of hallucinating.

#

Expected output (values will vary slightly by model run since even at
temperature 0 the model may phrase severity differently, but the *shape*
and the `null` on the missing phone number will always hold):

```json
{
  "customer_name": "Usman Tariq",
  "order_number": "ORD-9981",
  "complaint_type": "LATE_DELIVERY",
  "severity_level": 4,
  "contact_phone": null
}
```

## How it satisfies the project requirements

| Requirement | Where it lives |
|---|---|
| Strict delimiters (`"""`) separating instructions from raw data | `USER_TEMPLATE` wraps `{raw_data}` in `"""..."""` |
| Few-shot learning (2–3 perfect I/O pairs) | 3 examples embedded in `SYSTEM_PROMPT` |
| JSON-only output, no filler | Rule #1/#5 in the prompt + `response_mime_type="application/json"` + defensive fence-stripping in `extract_json()` |
| Deterministic formatting | `temperature=0.0`, `top_p=1.0` |
| Null-fallback for missing data | Rule #3 in the prompt, tested by the gatekeeper case (missing phone number) |
| Schema/type validation | `validate_schema()` checks types, enum values, and integer range |

## Swapping the model

The prompt itself (`SYSTEM_PROMPT` / `USER_TEMPLATE`) is provider-agnostic.
To use OpenAI or Anthropic instead of Gemini, keep the prompt text as-is and
just swap the API call in `extract_json()` for the equivalent client call
(`temperature=0` in all three).
