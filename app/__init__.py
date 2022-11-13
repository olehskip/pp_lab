from flask import Flask
app = Flask(__name__)

from app.views import family_budget
from app.views import personal_budget
from app.views import user

app.register_blueprint(user.user_blueprint)
app.register_blueprint(family_budget.family_budgets_blieprint)
app.register_blueprint(personal_budget.personal_budgets_blieprint)

