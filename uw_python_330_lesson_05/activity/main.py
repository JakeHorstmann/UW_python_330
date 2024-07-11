from flask import Flask
import os
from time import time

app = Flask(__name__)

@app.route("/")
def get_time():
    return str(round(time()))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)