#ident "@(#)$Format:LocalFoodAI:app.py:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$"
import os

path = os.path.expanduser('~/.streamlit')
os.makedirs(path, exist_ok=True)

with open(os.path.join(path, 'credentials.toml'), 'w') as f:
    f.write("[general]\nemail = \"\"\n")

with open(os.path.join(path, 'config.toml'), 'w') as f:
    f.write("[browser]\ngatherUsageStats = false\n")

print("Streamlit credentials and config written successfully!")
