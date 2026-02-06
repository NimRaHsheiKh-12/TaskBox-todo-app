import re

# Copy the FIXED patterns from the message parser
complete_patterns = [
    r"(complete|finish|done|completed|finished)\s+(?:the\s+)?(.+?)",
    r"(mark|set)\s+(?:the\s+)?(.+?)\s+(?:as\s+)?(complete|done|finished)",
    r"i\s+(?:have\s+)?(completed|finished|done)\s+(?:the\s+)?(.+?)",
    r"cross\s+(?:the\s+)?(.+?)\s+off\s+(?:my\s+)?(?:list|tasks)"
]

message = "mark buy groceries as completed"
message_lower = message.lower()

print(f"Testing message: '{message}'")
print()

for i, pattern in enumerate(complete_patterns):
    print(f"Pattern {i+1}: {pattern}")
    match = re.search(pattern, message_lower)
    if match:
        groups = match.groups()
        print(f"  Match found! Groups: {groups}")
        if len(groups) > 1:
            task_title = groups[1].strip()
            print(f"  Task title extracted: '{task_title}'")
        elif len(groups) == 1:
            task_title = groups[0].strip()
            print(f"  Task title extracted: '{task_title}'")
        else:
            print("  No groups found")
    else:
        print("  No match")
    print()