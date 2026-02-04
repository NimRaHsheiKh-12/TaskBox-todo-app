import re

pattern = r'complete\s+task\s+(\d+)'
msg = 'complete task 1'
match = re.search(pattern, msg)
print('Message:', repr(msg))
print('Pattern:', repr(pattern))
print('Match object:', match)
if match:
    print('Groups:', match.groups())
else:
    print('No match found')

# Also test the other pattern
pattern2 = r"complete\s+'([^']+)'"
match2 = re.search(pattern2, msg)
print('Pattern2:', repr(pattern2))
print('Match2 object:', match2)
if match2:
    print('Groups2:', match2.groups())
else:
    print('No match2 found')