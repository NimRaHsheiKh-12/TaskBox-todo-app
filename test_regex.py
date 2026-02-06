import re

message = "add buy milk"
message_lower = message.lower().strip()

create_patterns = [
    r"(add|create|make|new)\s+(?:a\s+|an\s+|the\s+)?(.+?)\s+to\s+my\s+list",
    r"(add|create|make|new)\s+(?:a\s+|an\s+|the\s+)?(.+?)\s+(?:to\s+my\s+)?(?:task|todo|to-do)\s+list",
    r"(add|create|make|new)\s+(.+)",
    r"i\s+need\s+to\s+(.+)",
    r"don'?t\s+forget\s+to\s+(.+)",
    r"remind\s+me\s+to\s+(.+)"
]

for pattern in create_patterns:
    if re.search(pattern, message_lower):
        print(f"Matched pattern: {pattern}")
        match = re.search(pattern, message_lower)
        print(f"Groups: {match.groups()}")
        break
else:
    print("No match")