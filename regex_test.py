import re

# Test the patterns
patterns = [
    r"(add|create|make|new)\s+(?:a\s+|an\s+|the\s+)?(.+?)\s+to\s+my\s+list",
    r"(add|create|make|new)\s+(?:a\s+|an\s+|the\s+)?(.+?)\s+(?:to\s+my\s+)?(?:task|todo|to-do)\s+list",
    r"(add|create|make|new)\s+(?:a\s+|an\s+|the\s+)?(.+)"
]

test_message = "Add 'Buy groceries' to my list"

print(f"Testing message: '{test_message}'")
for i, pattern in enumerate(patterns):
    match = re.search(pattern, test_message.lower())
    if match:
        groups = match.groups()
        print(f"Pattern {i+1}: {pattern}")
        print(f"  Match found: {match.group()}")
        print(f"  Groups: {groups}")
        if len(groups) > 1:
            print(f"  Extracted title: '{groups[1]}'")
        print()
    else:
        print(f"Pattern {i+1}: {pattern}")
        print("  No match found")
        print()