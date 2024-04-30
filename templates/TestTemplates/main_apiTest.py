from flask import Flask, render_template, request
from functions import * 

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("home.html")

@app.route("/apiTest", methods=["POST"])
def api_test():
    if request.method == "POST":
        if "google_APIKey_button" in request.form:
            google_APIKey_py = google_api_test(request.form["google_APIKey_input"])
            return render_template("home.html", google_APIKey_html=google_APIKey_py)
        elif "openAI_APIKey_button" in request.form:
            openAI_APIKey_py = openai_api_test(request.form["openAI_APIKey_input"])
            return render_template("home.html", openAI_APIKey_html=openAI_APIKey_py)

if __name__ == "__main__":
    app.run(debug=True)

