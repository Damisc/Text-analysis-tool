from flask import Flask


app = Flask(__name__)

@app.route("/route")

def hello_world():
    return "Flask Server is up and Running"

if __name__ == "__main__":
    app.run()