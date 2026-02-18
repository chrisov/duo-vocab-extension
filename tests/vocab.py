import json
from datetime import datetime, timezone
import urllib.request

def test_save_vocab():
    url = "http://localhost:5000/save-vocab"

    # Sample payload – adjust vocabulary/language as you like
    payload = {
        "vocabulary": ["hola", "adiós", "gracias", "Ei", "Maria", "o", "o seu", "sou" ],
        "timestamp": datetime.now(timezone.utc).isoformat(),  # like new Date().toISOString()
        "language": "pt"
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(req) as resp:
        body = resp.read().decode("utf-8")
        print("Status:", resp.status)
        print("Response:", body)

if __name__ == "__main__":
    test_save_vocab()