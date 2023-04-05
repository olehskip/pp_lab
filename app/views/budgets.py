from marshmallow import Schema, fields, ValidationError
from datetime import datetime
from flask import Blueprint, jsonify, request
import app.models as models
import app.db as db
from flask_bcrypt import Bcrypt
from app.auth import auth

budgets_blueprint = Blueprint('budgets', __name__, url_prefix='/api/budgets')
bcrypt = Bcrypt()

budgets_blueprint.route('/', methods=['GET'])
def get_all_budgets():
	budgets_json = []
	personal_budgets = db.session.query(models.PersonalBudgets).all()
	for personal_budget in personal_budgets:
		budget_json = {}
		budget_json['id'] = personal_budget.id
		budget_json['money_amount'] = personal_budget.money_amount
		budget_json['members'] = db.session.query(models.Users).filter_by(id=personal_budget.id).first().username
		budget_json['type'] = 'personal'
		budgets_json.append(budget_json)
		
	family_budgets = db.session.query(models.FamilyBudgets).all()
	for family_budget, _ in family_budgets:
		budget_json = {}
		budget_json['id'] = family_budget.id
		budget_json['money_amount'] = family_budget.money_amount
		budget_json['members'] = [user.username for user, _ in db.session.query(models.Users, models.FamilyBudgetsUsers).outerjoin(models.FamilyBudgetsUsers, models.FamilyBudgetsUsers.user_id==models.Users.id,).filter(models.FamilyBudgetsUsers.family_budget_id==family_budget.id).all()]

		budget_json['type'] = 'family'
		budgets_json.append(budget_json)
	return jsonify(budgets_json), 200