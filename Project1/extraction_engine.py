"""
Project 1: Zero-Shot & Few-Shot Data Extraction
DecodeLabs Prompt Engineering Kit

Author: Muhammad Fareed
"""
from openai import OpenAI
import os
import json

# =====================================================
# CONFIGURATION
# =====================================================

API_KEY = os.getenv("OPENROUTER_API_KEY")

# You can temporarily paste your key here for testing:
API_KEY = ""

if not API_KEY:
    raise EnvironmentError(
        "OPENROUTER_API_KEY not found."
    )

client = OpenAI(
    api_key=API_KEY,
    base_url="https://openrouter.ai/api/v1"
)

MODEL_NAME = "meta-llama/llama-3.3-70b-instruct"

# =====================================================
# SYSTEM PROMPT
# =====================================================
# NOTE: This string now uses ''' as the OUTER delimiter
# because the examples below contain """ blocks internally.
# Mixing """ inside a """-quoted string breaks Python syntax.

SYSTEM_PROMPT = '''
You are a deterministic data extraction engine.

Return ONLY valid JSON.

Extract exactly these fields:

{
  "customer_name": "string",
  "order_number": "string",
  "complaint_type": "LOGIN_FAILURE | LATE_DELIVERY | DAMAGED_ITEM | BILLING_ISSUE | REFUND_REQUEST | OTHER",
  "severity_level": "integer (1-5)",
  "contact_phone": "string or null"
}

Rules

1. Output ONLY JSON.
2. Never explain.
3. Never use markdown.
4. Never invent values.
5. Missing values MUST be null.
6. Infer complaint_type and severity_level from context.

--------------------------
Example 1

Input:

"""
Hi team, this is Sarah Malik.
My order ORD-7789 arrived completely damaged.
Please replace it.
Call me on 03001234567.
"""

Output

{
  "customer_name":"Sarah Malik",
  "order_number":"ORD-7789",
  "complaint_type":"DAMAGED_ITEM",
  "severity_level":4,
  "contact_phone":"03001234567"
}

--------------------------
Example 2

Input

"""
Ahmed Raza here.

Can't login.

Order ORD-1123.

Password reset keeps failing.
"""

Output

{
  "customer_name":"Ahmed Raza",
  "order_number":"ORD-1123",
  "complaint_type":"LOGIN_FAILURE",
  "severity_level":5,
  "contact_phone":null
}

--------------------------
Example 3

Input

"""
Fatima Sheikh.

Order ORD-4432.

I was charged twice.

Please refund the duplicate payment.
"""

Output

{
  "customer_name":"Fatima Sheikh",
  "order_number":"ORD-4432",
  "complaint_type":"BILLING_ISSUE",
  "severity_level":2,
  "contact_phone":null
}
'''

USER_TEMPLATE = '''
Extract information from the text below.

"""
{raw_data}
"""
'''

# =====================================================
# VALIDATION
# =====================================================

REQUIRED_FIELDS = {
    "customer_name": str,
    "order_number": str,
    "complaint_type": str,
    "severity_level": int,
    "contact_phone": (str, type(None))
}

VALID_TYPES = {
    "LOGIN_FAILURE",
    "LATE_DELIVERY",
    "DAMAGED_ITEM",
    "BILLING_ISSUE",
    "REFUND_REQUEST",
    "OTHER"
}


def validate_schema(data):

    for field, expected in REQUIRED_FIELDS.items():

        if field not in data:
            raise ValueError(f"Missing field: {field}")

        if not isinstance(data[field], expected):
            raise ValueError(
                f"{field} should be {expected}"
            )

    if data["complaint_type"] not in VALID_TYPES:
        raise ValueError("Invalid complaint type")

    if not (1 <= data["severity_level"] <= 5):
        raise ValueError("Severity level must be between 1 and 5")


# =====================================================
# EXTRACTION
# =====================================================

def extract_json(raw_text):

    prompt = USER_TEMPLATE.format(raw_data=raw_text)

    response = client.chat.completions.create(

        model=MODEL_NAME,

        temperature=0,

        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    output = response.choices[0].message.content.strip()

    # Remove markdown if present
    if output.startswith("```"):
        output = output.replace("```json", "")
        output = output.replace("```", "").strip()

    data = json.loads(output)

    validate_schema(data)

    return data


# =====================================================
# TEST EMAIL
# =====================================================

EMAIL = """
Subject: Order never arrived

Hello Support,

My name is Usman Tariq.

My order number is ORD-9981.

My parcel has still not arrived after five days.

My Phone number is 03007654321.

This is becoming very frustrating.

Please resolve it urgently.

Thank you.
"""

# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    result = extract_json(EMAIL)

    print("\nExtracted JSON:\n")

    print(json.dumps(result, indent=4))