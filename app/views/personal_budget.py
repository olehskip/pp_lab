from marshmallow import Schema, fields, ValidationError
#from marshmallow_enum import EnumField
from datetime import datetime
from enum import Enum
from flask import Blueprint, jsonify, request
import app.models as models
import app.db as db
from flask_bcrypt import Bcrypt

PersonalBudgets_blueprint = Blueprint('PersonalBudgets', __name__, url_prefix='/PersonalBudgets')
bcrypt = Bcrypt()

def from_Personal_model_to_json(personalBudget: models.PersonalBudgets):
	PersonalBudgets_json = {}
	
	PersonalBudgets_json['id'] = personalBudget.id
	PersonalBudgets_json['money_amount'] = personalBudget.money_amount
		
	return jsonify(PersonalBudgets_json)

@PersonalBudgets_blueprint.route('/<int:personalBudget_id>', methods=['GET'])
def get_personal_budget(personalBudget_id):
	personalBudget = db.session.query(models.PersonalBudgets).filter_by(id=personalBudget_id).first()
	if personalBudget is None:
		return jsonify({'error': 'Budget not found'}), 404

	return from_Personal_model_to_json(personalBudget), 200
	
@PersonalBudgets_blueprint.route('/<int:personalBudget_id>/report', methods=['GET'])
def get_personalBudget_report(personalBudget_id):
	user = db.session.query(models.Users).filter_by(id=personalBudget_id).first()
	if user is None:
		return jsonify({'error': 'User not found'}), 404
		
	report1 = db.session.query(models.Operation).filter(models.Operation.sender_id==personalBudget_id and models.Operation.sender_type=="personal").all()
	report2 = db.session.query(models.Operation).filter(models.Operation.receiver_id==personalBudget_id and receiver_type=="personal").all()
	if report1 is None and report2 is None:
		return jsonify({'error': 'This budget has no operations'}), 405
		
	report_json = []
	for oper in report1:
		operation = {}
		
		operation['id'] = oper.id
		operation['sender_id'] = oper.sender_id
		operation['receiver_id'] = oper.receiver_id
		operation['sender_type'] = oper.sender_type
		operation['receiver_type'] = oper.receiver_type
		operation['money_amount'] = oper.money_amount
		operation['date'] = oper.date
		
		report_json.append(operation)
		
	for oper in report2:
		operation = {}
		
		operation['id'] = oper.id
		operation['sender_id'] = oper.sender_id
		operation['receiver_id'] = oper.receiver_id
		operation['sender_type'] = oper.sender_type
		operation['receiver_type'] = oper.receiver_type
		operation['money_amount'] = oper.money_amount
		operation['date'] = oper.date
		
		report_json.append(operation)	
		
	return jsonify(report_json), 200
	
@PersonalBudgets_blueprint.route('/<int:personalBudget_id>/transfer', methods=['POST'])
def post_personalBudget_transfer(personalBudget_id):
	personalBudget = db.session.query(models.PersonalBudgets).filter_by(id=personalBudget_id).first()
	if personalBudget is None:
		return jsonify({'error': 'User not found'}), 404
		
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
		
	if request.json['money_amount'] < 0.1:
		return jsonify({'error': 'Money amount couldn`t be less than 0.1'}), 407
	
	if personalBudget.money_amount < request.json['money_amount']:
		return jsonify({'error': 'Not enough money'}), 406
	
	now = datetime.now()
	operation = models.Operation(sender_id=personalBudget_id, receiver_id=request.json['receiver_budget_id'], sender_type="personal", receiver_type=request.json['receiver_type'],money_amount=request.json['money_amount'],date=now)
	
	try:
		db.session.add(operation)
	except:
		return jsonify({'error': 'Failed to execute operation, database error'}), 405
	
	if request.json['receiver_type'] == "personal":
		receiver_budget = db.session.query(models.PersonalBudgets).filter_by(id=request.json['receiver_budget_id']).first()
		if receiver_budget is None:
			db.session.rollback()
			return jsonify({'error': 'Receiving budget doesn`t exist'}), 408
		receiver_budget.money_amount = receiver_budget.money_amount + request.json['money_amount']
	
	else:
		receiver_budget = db.session.query(models.FamilyBudgets).filter_by(id=request.json['receiver_budget_id']).first()
		if receiver_budget is None:
			db.session.rollback()
			return jsonify({'error': 'Receiving budget doesn`t exist'}), 408
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
	
	
		
	
		
	
	


