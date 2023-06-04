from marshmallow import Schema, fields, ValidationError
from datetime import datetime
from flask import Blueprint, jsonify, request
import app.models as models
import app.db as db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import (
	jwt_required, get_jwt_identity
)

budgets_blueprint = Blueprint('budgets', __name__, url_prefix='/api/budgets')
bcrypt = Bcrypt()

@budgets_blueprint.route('/<string:username>', methods=['GET'])
@jwt_required()
def get_all_budgets(username):
	user = db.session.query(models.Users).filter_by(username=username).first()
	current_user_id = get_jwt_identity()
	current_user = db.session.query(models.Users).filter_by(id=current_user_id).first()

	if user is None:
		return jsonify({'error': 'User not found'}), 404
	
	if user.id != current_user_id and not current_user.is_admin:
		return jsonify({'error': 'Forbidden'}), 403

	budgets_json = []
	personal_budgets = db.session.query(models.PersonalBudgets).filter_by(id=user.id).all()
	for personal_budget in personal_budgets:
		budget_json = {}
		budget_json['id'] = personal_budget.id
		budget_json['money_amount'] = personal_budget.money_amount
		budget_json['members'] = [db.session.query(models.Users).filter_by(id=personal_budget.id).first().username]
		budget_json['type'] = 'personal'
		budgets_json.append(budget_json)
		
	family_budgets = db.session.query(models.FamilyBudgets, models.FamilyBudgetsUsers).outerjoin(models.FamilyBudgetsUsers, models.FamilyBudgetsUsers.family_budget_id==models.FamilyBudgets.id,).filter(models.FamilyBudgetsUsers.user_id==user.id).all()
	for family_budget, _ in family_budgets:
		budget_json = {}
		budget_json['id'] = family_budget.id
		budget_json['money_amount'] = family_budget.money_amount
		budget_json['members'] = [user.username for user, _ in db.session.query(models.Users, models.FamilyBudgetsUsers).outerjoin(models.FamilyBudgetsUsers, models.FamilyBudgetsUsers.user_id==models.Users.id,).filter(models.FamilyBudgetsUsers.family_budget_id==family_budget.id).all()]

		budget_json['type'] = 'family'
		budgets_json.append(budget_json)

	return jsonify(budgets_json), 200

@budgets_blueprint.route('', methods=['GET'])
@jwt_required()
def get_all_my_budgets():
	user_id = get_jwt_identity()
	user = db.session.query(models.Users).filter_by(id=user_id).first()

	if user is None:
		return jsonify({'error': 'User not found'}), 404
	
	return get_all_budgets(user.username)

@budgets_blueprint.route('/transfer_money', methods=['POST'])
@jwt_required()
def transfer_money():
	user_id = get_jwt_identity()
	user = db.session.query(models.Users).filter_by(id=user_id).first()

	if user is None:
		return jsonify({'error': 'User not found'}), 404

	class TransferMoneySchema(Schema):
		from_budget_id = fields.Int(required=True)
		from_budget_type = fields.Str(required=True)
		to_budget_id = fields.Int(required=True)
		to_budget_type = fields.Str(required=True)
		money_amount = fields.Int(required=True)

	try:
		transfer_money_schema = TransferMoneySchema()
		transfer_money_schema.load(request.json)
	except ValidationError as err:
		return jsonify(err.messages), 400
	
	from_budget_id = request.json['from_budget_id']
	from_budget_type = request.json['from_budget_type']
	to_budget_id = request.json['to_budget_id']
	to_budget_type = request.json['to_budget_type']
	money_amount = request.json['money_amount']

	if from_budget_type == 'personal':
		from_budget = db.session.query(models.PersonalBudgets).filter_by(id=from_budget_id).first()
	elif from_budget_type == 'family':
		from_budget = db.session.query(models.FamilyBudgets).filter_by(id=from_budget_id).first()
	else:
		return jsonify({'error': 'Invalid budget type'}), 400
	
	if to_budget_type == 'personal':
		to_budget = db.session.query(models.PersonalBudgets).filter_by(id=to_budget_id).first()
	elif to_budget_type == 'family':
		to_budget = db.session.query(models.FamilyBudgets).filter_by(id=to_budget_id).first()
	else:
		return jsonify({'error': 'Invalid budget type'}), 400
	
	if from_budget is None or to_budget is None:
		return jsonify({'error': 'Budget not found'}), 404
	
	if from_budget_type == 'personal' and from_budget.id != user.id:
		return jsonify({'error': 'Forbidden'}), 403
	
	if to_budget_type == 'personal' and to_budget.id != user.id:
		return jsonify({'error': 'Forbidden'}), 403
	
	if from_budget.money_amount < money_amount:
		return jsonify({'error': 'Not enough money'}), 400
	
	if money_amount < 0:
		return jsonify({'error': 'Invalid money amount'}), 400

	from_budget.money_amount -= money_amount
	to_budget.money_amount += money_amount
	db.session.commit()


	return "", 204
