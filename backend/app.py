from pathlib import Path
from flask import Flask, render_template

BASE_DIR = Path(__file__).resolve().parent
PROJECT_DIR = BASE_DIR.parent

TEMPLATE_DIR = PROJECT_DIR / "frontend" / "templates"
STATIC_DIR = PROJECT_DIR / "frontend" / "static"

app = Flask(
    __name__,
    template_folder=str(TEMPLATE_DIR),
    static_folder=str(STATIC_DIR)
)

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/detection")
def detection():
    return render_template("detection.html")


@app.route("/analytics")
def analytics():
    return render_template("analytics.html")

if __name__ == "__main__":
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True
    )
