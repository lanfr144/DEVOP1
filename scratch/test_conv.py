import re

line1 = '#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"'
line2 = '#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"'
line3 = '#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"'

pattern = r':(\d{4}/\d{2}/\d{2} \d{2}:\d{2}:\d{2}):([0-9a-fA-F]{40}|Not Committed Yet):'

for i, line in enumerate([line1, line2, line3]):
    m = re.search(pattern, line)
    if m:
        print(f"Line {i+1} matched: Date={m.group(1)}, Hash={m.group(2)}")
    else:
        print(f"Line {i+1} did not match")
