from marshmallow import Schema, fields, ValidationError
from datetime import datetime
from enum import Enum
from flask import Blueprint, jsonify, request
import app.models as models
import app.db as db
from flask_bcrypt import Bcrypt
from app.auth import auth
from sqlalchemy import or_
from flask_jwt_extended import (
	jwt_required, get_jwt_identity
)

personal_budgets_blieprint = Blueprint('PersonalBudgets', __name__, url_prefix='/api/personal_budget')
bcrypt = Bcrypt()

@personal_budgets_blieprint.route('/<int:personal_budget_id>', methods=['GET'])
@jwt_required()
def get_personal_budget(personal_budget_id):
	print("called")
	user_id = get_jwt_identity()
	print("user_id", user_id)
	user = db.session.query(models.Users).filter_by(id=user_id).first()
	
	if user is None:
		return jsonify({'error': 'User not found'}), 404

	if personal_budget_id != user_id:
		return jsonify({'error': 'Forbidden'}), 403
	
	personal_budget = db.session.query(models.PersonalBudgets).filter_by(id=personal_budget_id).first()

	personal_budget_json = {}
	personal_budget_json['id'] = personal_budget.id
	personal_budget_json['members'] = [user.username]
	personal_budget_json['money'] = personal_budget.money_amount
	personal_budget_json['type'] = 'personal'
		
	return jsonify(personal_budget_json), 200

@personal_budgets_blieprint.route('/<int:personal_budget_id>/report', methods=['GET'])
@jwt_required()
def get_personal_budget_report(personal_budget_id):
	if personal_budget_id != auth.current_user().id:
		return jsonify({'error': 'Forbidden'}), 403

	report_json = []
	reports = db.session.query(models.Operation).filter(models.Operation.sender_type=="personal").filter(or_(
		models.Operation.sender_id==personal_budget_id, models.Operation.receiver_id==personal_budget_id)).all()
		
	for operation in reports:
		operation_json = {}
		
		operation_json['id'] = operation.id
		operation_json['sender_id'] = operation.sender_id
		operation_json['receiver_id'] = operation.receiver_id
		operation_json['sender_type'] = operation.sender_type
		operation_json['receiver_type'] = operation.receiver_type
		operation_json['money_amount'] = operation.money_amount
		operation_json['date'] = operation.date
		
		report_json.append(operation_json)

	return jsonify(report_json), 200
	
@personal_budgets_blieprint.route('/<int:personal_budget_id>/transfer', methods=['POST'])
@jwt_required()
def post_personal_budget_transfer(personal_budget_id):
	if personal_budget_id != auth.current_user().id:
		return jsonify({'error': 'Forbidden'}), 403

	personalBudget = db.session.query(models.PersonalBudgets).filter_by(id=personal_budget_id).first()

	class Transfer(Schema):
		receiver_budget_id = fields.Int(required=True)
		receiver_type = fields.Str(required=True)
		money_amount = fields.Int(required=True)
		
	try:
		if not request.json:
			raise ValidationError('No input data provided')
		Transfer().load(request.json)
	except ValidationError as err:
		return jsonify(err.messages), 400
		
	if request.json['money_amount'] < 1:
		return jsonify({'error': 'Money amount couldn`t be less than 1'}), 400
	
	if personalBudget.money_amount < request.json['money_amount']:
		return jsonify({'error': 'Not enough money'}), 400
	
	now = datetime.now()
	operation = models.Operation(sender_id=personal_budget_id, receiver_id=request.json['receiver_budget_id'], sender_type="personal", receiver_type=request.json['receiver_type'],money_amount=request.json['money_amount'],date=now)
	
	db.session.add(operation)
	
	if request.json['receiver_type'] == "personal":
		receiver_budget = db.session.query(models.PersonalBudgets).filter_by(id=request.json['receiver_budget_id']).first()
		if receiver_budget is None:
			db.session.rollback()
			return jsonify({'error': 'Receiving budget doesn`t exist'}), 400
		receiver_budget.money_amount = receiver_budget.money_amount + request.json['money_amount']
	
	else:
		receiver_budget = db.session.query(models.FamilyBudgets).filter_by(id=request.json['receiver_budget_id']).first()
		if receiver_budget is None:
			db.session.rollback()
			return jsonify({'error': 'Receiving budget doesn`t exist'}), 400
		receiver_budget.money_amount = receiver_budget.money_amount + request.json['money_amount']
	
	personalBudget.money_amount = personalBudget.money_amount - request.json['money_amount']
	db.session.commit()
	
	operation_json = {}
	
	operation_json['id'] = operation.id
	operation_json['sender_id'] = operation.sender_id
	operation_json['receiver_id'] = operation.receiver_id
	operation_json['sender_type'] = operation.sender_type
	operation_json['receiver_type'] = operation.receiver_type
	operation_json['money_amount'] = operation.money_amount
	operation_json['date'] = operation.date
	
	return jsonify(operation_json), 200

