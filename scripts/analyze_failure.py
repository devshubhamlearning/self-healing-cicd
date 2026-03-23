import os
import sys
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

def analyze_failure(logs: str) -> dict:
    """
    Sends failure logs to LLM and gets:
    - Root cause
    - Fix suggestion
    - Auto-fixable (yes/no)
    """
    client = Groq(api_key=os.getenv("GROQ_API_KEY"))

    prompt = f"""You are an expert DevOps engineer analyzing a CI/CD pipeline failure.

Here are the failure logs:
{logs}

Respond in this exact format:
ROOT_CAUSE: <one line explanation>
FIX: <exact code or command to fix it>
AUTO_FIXABLE: <yes or no>
FILE_TO_FIX: <filename if code fix needed, else none>
"""

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    raw = response.choices[0].message.content
    print(f"\n�� AI Analysis:\n{raw}\n")

    result = {}
    for line in raw.strip().split("\n"):
        if ":" in line:
            key, val = line.split(":", 1)
            result[key.strip()] = val.strip()

    return result


if __name__ == "__main__":
    # Read logs from stdin or argument
    if len(sys.argv) > 1:
        logs = open(sys.argv[1]).read()
    else:
        logs = sys.stdin.read()

    result = analyze_failure(logs)
    print(f"Root Cause: {result.get('ROOT_CAUSE')}")
    print(f"Fix: {result.get('FIX')}")
    print(f"Auto Fixable: {result.get('AUTO_FIXABLE')}")
