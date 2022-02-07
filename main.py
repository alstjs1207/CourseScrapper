from flask import Flask, render_template, request, send_file
from werkzeug.utils import redirect
from functions import getCourses
from export import export
from db import languages, db


app = Flask(__name__, template_folder="templates")


@app.route("/")
def main():
    word = request.args.get("word")

    if not word:
        return render_template("index.html", languages=languages)

    word = word.lower()
    fromdB = db.get(word)
    if fromdB:
        courses = fromdB
    else:
        courses = getCourses(word)
            
    count = len(courses)
    db[word] = courses

    return render_template("result.html", courses=courses, word=word, count=count)


@app.route("/search")
def search():
    word = request.args["word"].lower()

    fromDB = db.get(word)
    if fromDB:
        courses = fromDB
    else:
        courses = getCourses(word)
    
    count = len(courses)
    db[word] = courses

    return render_template("result.html", courses=courses, word=word, count=count)


@app.route("/export")
def file():

    word = request.args.get("word")
    if not word:
        raise Exception()
    word = word.lower()
    courses = db.get(word)
    if not courses:
        raise Exception()
    export(word)
    return send_file("courses.csv")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="8282", debug=True)
