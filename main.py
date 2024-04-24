from flask import Flask, render_template

app = Flask(__name__)

# When the url "/" is accessed, then return the string.
@app.route("/")
def greeting():
    return render_template("home.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug = True)