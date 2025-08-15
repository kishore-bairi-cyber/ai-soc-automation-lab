
---

## ⚙️ Python Automation Script

Saved in: `parse_header.py`

Basic parser to extract key values from header:

```python
import email
import re

def parse_header(header_str):
    parsed = {}
    ip_match = re.findall(r'\[(\d+\.\d+\.\d+\.\d+)\]', header_str)
    from_match = re.search(r'From: (.*)', header_str)
    replyto_match = re.search(r'Reply-To: (.*)', header_str)

    parsed['Sender_IPs'] = ip_match
    parsed['From'] = from_match.group(1) if from_match else 'N/A'
    parsed['Reply-To'] = replyto_match.group(1) if replyto_match else 'N/A'
    return parsed

# Example usage
header = open('sample_email_header.txt').read()
print(parse_header(header))
