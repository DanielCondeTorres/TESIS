import re

with open("references.bib", "r") as f:
    content = f.read()

content = re.sub(r"\n\s*volume\s*=\s*\{0\},?", "", content, flags=re.IGNORECASE)
content = re.sub(r"\n\s*numpages\s*=\s*\{0\},?", "", content, flags=re.IGNORECASE)
content = re.sub(r"\n\s*issue\s*=\s*\{0\},?", "", content, flags=re.IGNORECASE)

with open("references.bib", "w") as f:
    f.write(content)

print("Cleaned 0 fields")
