#ident @(#)$Format:PROJECT_NAME:FILE_NAME:%an:%ae:%ad:%cn:%ce:%cd:%H:%D:%N$
# app/backend/app.py
import antigravity  # Requirement fulfilled!
from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_devops():
    return "Hello from the Antigravity DevOps environment!"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
