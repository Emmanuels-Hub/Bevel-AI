from flask import render_template, request, Blueprint

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def index():
    return render_template('index.html')


@main.route("/api")
def api():
    return render_template('api.html')