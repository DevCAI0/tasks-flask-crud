from flask import Flask

app = Flask(__name__)

@app.route("/")
def hellow_world():
    return "hello world!"
@app.route("/sobre")
def sobre():
    return "Pagina Sobre"
if __name__ == "__main__":
    app.run(debug=True)