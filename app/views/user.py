from marshmallow import Schema, fields, ValidationError, validate
from flask import Blueprint, jsonify, request
import app.models as models
import app.db as db
from flask_bcrypt import Bcrypt
from app.auth import auth
from flask_jwt_extended import (
    jwt_required, get_jwt_identity, create_access_token
)

user_blueprint = Blueprint('user', __name__, url_prefix='/api/user')
bcrypt = Bcrypt()
	
@user_blueprint.route('/all', methods=['GET'])
@jwt_required()
def get_all_users():
	user_id = get_jwt_identity()
	user = db.session.query(models.Users).filter_by(id=user_id).first()

	if user is None:
		return jsonify({'error': 'User not found'}), 404

	if not user.is_admin:
		return jsonify({'error': 'Forbidden'}), 403
	
	users = db.session.query(models.Users).all()
	res_json = []
	for user in users:
		user_json = {}
		user_json['username'] = user.username
		res_json.append(user_json)
	return jsonify(res_json), 200

@user_blueprint.route('/all', methods=['DELETE'])
@jwt_required()
def delete_user():
	user_id = get_jwt_identity()
	user = db.session.query(models.Users).filter_by(id=user_id).first()

	if user is None:
		return jsonify({'error': 'User not found'}), 404

	if not user.is_admin:
		return jsonify({'error': 'Forbidden'}), 403

	class User(Schema):
		username = fields.Str(required=True)

	try:
		if not request.json:
			raise ValidationError('No input data provided')
		User().load(request.json)
	except ValidationError as err:
		return jsonify(err.messages), 400
	
	user_to_delete = db.session.query(models.Users).filter_by(username=request.json['username']).first()
	if user_to_delete is None:
		return jsonify({'error': 'User not found'}), 404
	
	if user_to_delete.is_admin:
		return jsonify({'error': 'Forbidden'}), 403
	
	db.session.delete(user_to_delete)
	db.session.commit()

	return "", 204


@user_blueprint.route('', methods=['POST'])
def create_user():
	class User(Schema):
		surname = fields.Str(required=True, validate=[validate.Length(min=6, max=50)])
		name = fields.Str(required=True, validate=[validate.Length(min=6, max=50)])
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
		return jsonify({'error': 'User already exists'}), 409

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

@user_blueprint.route('/', methods=['GET'])
@jwt_required()
def get_current_user():
	user_id = get_jwt_identity()
	user = db.session.query(models.Users).filter_by(id=user_id).first()

	if user is None:
		return jsonify({'error': 'User not found'}), 404
	
	res_json = {}

	res_json['id'] = user.id
	res_json['surname'] = user.surname
	res_json['name'] = user.name
	res_json['username'] = user.username
	res_json['personal_budget'] = user.id
	res_json['family_budgets'] = [int(row.family_budget_id) for row in db.session.query(models.FamilyBudgetsUsers).filter_by(user_id=user_id).all()]

	return jsonify(res_json), 200

@user_blueprint.route('/', methods=['PATCH'])
@jwt_required()
def update_current_user():
	user_id = get_jwt_identity()
	user = db.session.query(models.Users).filter_by(id=user_id).first()

	if user is None:
		return jsonify({'error': 'User not found'}), 404
	
	class User(Schema):
		surname = fields.Str(required=False, validate=[validate.Length(max=50)])
		name = fields.Str(required=False, validate=[validate.Length(max=50)])
		username = fields.Str(required=False, validate=[validate.Length(max=50)])
		password = fields.Str(required=False, validate=[validate.Length(max=50)])

	try:
		if not request.json:
			raise ValidationError('No input data provided')
		User().load(request.json)
	except ValidationError as err:
		return jsonify(err.messages), 400
	
	
	if 'username' in request.json and not request.json['username'] == user.username:
		user_already_exists = db.session.query(models.Users).filter(models.Users.username == request.json['username']).count() != 0
		if user_already_exists:
			return jsonify({'error': 'User already exists'}), 409


	if 'surname' in request.json and len(request.json['surname']) > 0:
		user.surname = request.json['surname']
	if 'name' in request.json and len(request.json['name']) > 0:
		user.name = request.json['name']
	if 'username' in request.json and len(request.json['username']) > 0:
		user.username = request.json['username']
	if 'password' in request.json and len(request.json['password']) > 0:
		user.password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')

	db.session.commit()

	return jsonify({'message': 'User updated successfully'}), 200

@user_blueprint.route('/', methods=['DELETE'])
@jwt_required()
def delete_current_user():
	user_id = get_jwt_identity()
	user = db.session.query(models.Users).filter_by(id=user_id).first()

	if user is None:
		return jsonify({'error': 'User not found'}), 404
	
	db.session.delete(user)
	db.session.commit()

	return jsonify({'message': 'User deleted successfully'}), 200

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

@user_blueprint.route('/<int:user_id>', methods=['PATCH'])
@auth.login_required
def update_user(user_id):	
	try:
		class User(Schema):
			surname = fields.Str(required=False, validate=[validate.Length(max=50)])
			name = fields.Str(required=False, validate=[validate.Length(max=50)])
			username = fields.Str(required=False, validate=[validate.Length(max=50)])
			password = fields.Str(required=False, validate=[validate.Length(max=50)])
			
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
	
	if 'name' in request.json and len(request.json['name']) > 0:
		user.name = request.json['name']
	if 'username' in request.json and len(request.json['username']) > 0:
		user.username = request.json['username']
	if 'password' in request.json and len(request.json['password']) > 0:
		user.password = bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
	if 'surname' in request.json and len(request.json['surname']) > 0:
		user.surname = request.json['surname']

	db.session.commit()

	return "", 204
	
# @user_blueprint.route('/<int:user_id>', methods=['DELETE'])
# @auth.login_required
# def delete_user(user_id):
# 	user = db.session.query(models.Users).filter(models.Users.id == user_id).first()
	
# 	if user is None:
# 		return jsonify({'error': 'User does not exist'}), 404

# 	if user != auth.current_user():
# 		return jsonify({'error': 'Forbidden'}), 403
	
# 	db.session.delete(user)	
# 	db.session.commit()

# 	return "", 204

@user_blueprint.route("/login", methods=["POST"])
def login():
	try:
		class User(Schema):
			username = fields.Str(required=True, validate=[validate.Length(min=1, max=50)])
			password = fields.Str(required=True, validate=[validate.Length(min=1, max=50)])
			
		if not request.json:
			raise ValidationError('No input data provided')
		User().validate(request.json)
	except ValidationError as err:
		return jsonify(err.messages), 400

	user = db.session.query(models.Users).filter_by(username=request.json['username']).first()
	if user is None:
		return jsonify({'error': 'User not found'}), 404

	if not bcrypt.check_password_hash(user.password, request.json['password']):
		return jsonify({'error': 'Incorrect password'}), 401
	
	token = create_access_token(identity=user.id)
	return jsonify({'token': token, 'user_id':user.id}), 200

@user_blueprint.route("/register", methods=["POST"])
def register():
	try:
		class User(Schema):
			surname = fields.Str(required=True, validate=[validate.Length(min=6, max=50)])
			name = fields.Str(required=True, validate=[validate.Length(min=6, max=50)])
			username = fields.Str(required=True, validate=[validate.Length(min=6, max=50)])
			password = fields.Str(required=True, validate=[validate.Length(min=6, max=50)])
			
		if not request.json:
			raise ValidationError('No input data provided')
		User().load(request.json)
	except ValidationError as err:
		return jsonify(err.messages), 400

	user = db.session.query(models.Users).filter_by(username=request.json['username']).first()
	if user is not None:
		return jsonify({'error': 'User already exists'}), 409

	new_user_model = models.Users(
		surname=request.json['surname'],
		name=request.json['name'],
		username=request.json['username'],
		password=bcrypt.generate_password_hash(request.json['password']).decode('utf-8')
	)
	db.session.add(new_user_model)
	db.session.commit()
	
	new_personal_budget = models.PersonalBudgets(id=new_user_model.id, money_amount=0)
	db.session.add(new_personal_budget)
	db.session.commit()
	return login()
