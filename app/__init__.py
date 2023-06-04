from flask import Flask, render_template
from app import config
# from flask import send_file

app = Flask(__name__, static_url_path='', static_folder="../dist")


@app.route('/', defaults={'path': ''})
@app.route('/<string:path>')
@app.route('/<path:path>')
def index(path):
    return app.send_static_file('index.html')

@app.errorhandler(404)
def not_found(e):
    return app.send_static_file('index.html')


app.config['DATABASE_STR'] = 'postgresql://admin:admin@localhost/pp'
if config.is_testing:
    app.config['DATABASE_STR'] = 'sqlite:///test.db'

from app.views import family_budget
from app.views import personal_budget
from app.views import user
from app.views import budgets

app.register_blueprint(user.user_blueprint)
app.register_blueprint(family_budget.family_budgets_blieprint)
app.register_blueprint(personal_budget.personal_budgets_blieprint)
app.register_blueprint(budgets.budgets_blueprint)
