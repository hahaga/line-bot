from flask import Flask
app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World!"

@app.route("/test")
def test_endpoint():
    return "This is only a test"

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port='8081')