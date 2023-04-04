from marshmallow import Schema, fields, ValidationError
from flask import Blueprint, jsonify, request
import app.models as models
import app.db as db
from flask_bcrypt import Bcrypt
from app.auth import auth

user_blueprint = Blueprint('user', __name__, url_prefix='/api/user')
bcrypt = Bcrypt()
	
@user_blueprint.route('', methods=['GET'])
def get_all_users():
	users = db.session.query(models.Users).all()
	res_json = []
	for user in users:
		user_json = {}
		user_json['username'] = user.username
		res_json.append(user_json)
	return jsonify(res_json), 200

@user_blueprint.route('', methods=['POST'])
def create_user():
	print("received request", request.json)
	class User(Schema):
		surname = fields.Str(required=True)
		name = fields.Str(required=True)
		username = fields.Str(required=True)
		password = fields.Str(required=True)
		
	try:
		if not request.json:
			raise ValidationError('No input data provided')
		User().load(request.json)
	except ValidationError as err:
		return jsonify(err.messages), 400	


	new_user_model = models.Users(surname = request.json['surname'], name = request.json['name'], username = request.json['username'], password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8'))   
	user_already_exists = db.session.query(models.Users).filter(models.Users.username == new_user_model.username).count() != 0
	
	if user_already_exists:
		return jsonify({'error': 'User already exists'}), 400

	db.session.add(new_user_model)
	db.session.commit()
	
	new_personal_budget_model = models.PersonalBudgets(id=new_user_model.id, money_amount=10)
	
	db.session.add(new_personal_budget_model)
	db.session.commit()

	res_json = {}
	
	res_json['id'] = new_user_model.id
	res_json['surname'] = new_user_model.surname
	res_json['name'] = new_user_model.name
	res_json['username'] = new_user_model.username
	res_json['personal_budget'] = new_user_model.id

	return jsonify(res_json), 201

@user_blueprint.route('/<int:user_id>', methods=['GET'])
# @auth.login_required
def get_user(user_id):
	user = db.session.query(models.Users).filter_by(id=user_id).first()
	
	if user is None:
		return jsonify({'error': 'User not found'}), 404

	# if user != auth.current_user():
	# 	return jsonify({'error': 'Forbidden'}), 403
	
	res_json = {}
	
	res_json['id'] = user.id
	res_json['surname'] = user.surname
	res_json['name'] = user.name
	res_json['username'] = user.username
	res_json['personal_budget'] = user.id
	res_json['family_budgets'] = [int(row.family_budget_id) for row in db.session.query(models.FamilyBudgetsUsers).filter_by(user_id=user_id).all()]

	return jsonify(res_json), 200

@user_blueprint.route('/<int:user_id>/budgets', methods=['GET'])
def get_user_budgets(user_id):
	user = db.session.query(models.Users).filter_by(id=user_id).first()
	
	if user is None:
		return jsonify({'error': 'User not found'}), 404

	# if user != auth.current_user():
	# 	return jsonify({'error': 'Forbidden'}), 403
	
	budgets_json = []
	personal_budgets = db.session.query(models.PersonalBudgets).filter_by(id=user_id).all()
	for personal_budget in personal_budgets:
		budget_json = {}
		budget_json['id'] = personal_budget.id
		budget_json['money_amount'] = personal_budget.money_amount
		budget_json['members'] = db.session.query(models.Users).filter_by(id=personal_budget.id).first().username
		budget_json['type'] = 'personal'
		budgets_json.append(budget_json)
		
	family_budgets = db.session.query(models.FamilyBudgets, models.FamilyBudgetsUsers).outerjoin(models.FamilyBudgetsUsers, models.FamilyBudgetsUsers.family_budget_id==models.FamilyBudgets.id,).filter(models.FamilyBudgetsUsers.user_id==user_id).all()
	for family_budget, _ in family_budgets:
		budget_json = {}
		budget_json['id'] = family_budget.id
		budget_json['money_amount'] = family_budget.money_amount
		budget_json['members'] = [user.username for user, _ in db.session.query(models.Users, models.FamilyBudgetsUsers).outerjoin(models.FamilyBudgetsUsers, models.FamilyBudgetsUsers.user_id==models.Users.id,).filter(models.FamilyBudgetsUsers.family_budget_id==family_budget.id).all()]

		budget_json['type'] = 'family'
		budgets_json.append(budget_json)
	return jsonify(budgets_json), 200

@user_blueprint.route('/<int:user_id>', methods=['PATCH'])
@auth.login_required
def update_user(user_id):	
	try:
		class User(Schema):
			surname = fields.Str(required=False)
			name = fields.Str(required=False)
			username = fields.Str(required=False)
			password = fields.Str(required=False)
			
		if not request.json:
			raise ValidationError('No input data provided')
		User().load(request.json)
	except ValidationError as err:
		return jsonify(err.messages), 400
		
	user = db.session.query(models.Users).filter(models.Users.id == user_id).first()

	if user is None:
		return jsonify({'error': 'User not found'}), 404

	if user != auth.current_user():
		return jsonify({'error': 'Unauthorized access'}), 403
	
	if 'name' in request.json:
		user.name = request.json['name']
	if 'username' in request.json:
		user.username = request.json['username']
	if 'password' in request.json:
		user.password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
	if 'surname' in request.json:
		user.surname = request.json['surname']

	db.session.commit()

	return "", 204
	
@user_blueprint.route('/<int:user_id>', methods=['DELETE'])
@auth.login_required
def delete_user(user_id):
	user = db.session.query(models.Users).filter(models.Users.id == user_id).first()
	
	if user is None:
		return jsonify({'error': 'User does not exist'}), 404

	if user != auth.current_user():
		return jsonify({'error': 'Forbidden'}), 403
	
	db.session.delete(user)	
	db.session.commit()

	return "", 204

