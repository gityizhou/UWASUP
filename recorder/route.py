from flask import render_template


def hello():
    output = "Hello guys"

    return render_template("index.html", output=output)
