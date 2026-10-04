import os
from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Sikeres Flask Deploy a Railway-en! 🐍🚀</h1>"

if __name__ == '__main__':
    # A Railway által megadott PORT környezeti változót használjuk
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
