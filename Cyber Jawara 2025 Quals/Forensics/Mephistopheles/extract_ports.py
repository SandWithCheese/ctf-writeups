
filename = 'sysmon.txt'
with open(filename, 'r') as f:
    text = f.read()

# Find occurrences of DestinationPort
import re
# Pattern: DestinationPort\n(.*?)\nDestinationPortName
blocks = re.findall(r'DestinationPort\n(.*?)\nDestinationPortName', text, re.DOTALL)

interesting_ports = []
for b in blocks:
    b = b.strip()
    if b:
        interesting_ports.append(b)

from collections import Counter
print(Counter(interesting_ports))
