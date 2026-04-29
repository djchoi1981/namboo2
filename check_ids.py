import re

with open('/Users/djchoi81/Desktop/church-schedule-app/app.js', 'r') as f:
    js = f.read()

with open('/Users/djchoi81/Desktop/church-schedule-app/index.html', 'r') as f:
    html = f.read()

ids = re.findall(r"document\.getElementById\('([^']+)'\)", js)
missing = []
for idx in ids:
    if f'id="{idx}"' not in html and f"id='{idx}'" not in html:
        missing.append(idx)

if missing:
    print("MISSING IDs:", set(missing))
else:
    print("ALL IDs FOUND")
