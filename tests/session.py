import json
import urllib.request

def main():
    url = "http://localhost:5000/save-session"
    payload = {
        "language": "gr",
        "timestamp": "2026-04-10T21:20:52.791Z",
        "active": True
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
    main()