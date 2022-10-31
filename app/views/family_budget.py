from marshmallow import Schema, fields, ValidationError
#from marshmallow_enum import EnumField
from datetime import datetime
from enum import Enum
from flask import Blueprint, jsonify, request
import app.models as models
import app.db as db
from flask_bcrypt import Bcrypt

FamilyBudgets_blueprint = Blueprint('FamilyBudgets', __name__, url_prefix='/FamilyBudgets')
bcrypt = Bcrypt()

@FamilyBudgets_blueprint.route('/', methods=['POST'])
def create_new_familyBudget():
	class members_ids_class(Schema):
		member_ids = fields.List(fields.Int(), required=True)	
		
	members_ids_class().load(request.json)	
	try:
		if not request.json:
			raise ValidationError('No input data provided')
		members_ids_class().load(request.json)
	except ValidationError as err:
		return jsonify(err.messages), 400
		
	familyBudget = models.FamilyBudgets(money_amount=0)
	try:
		db.session.add(familyBudget)
	except:
		db.session.rollback()
		return jsonify({"Datbase error, failed to add family budget"}), 405
	db.session.commit()
		
	for member_id in request.json['member_ids']:
		familyBudgetUser = models.FamilyBudgetsUsers(family_budget_id=familyBudget.id, user_id=member_id)
		try:
			db.session.add(familyBudgetUser)
		except:
			db.session.rollback()
			return jsonify({"Datbase error, failed to add family member"}), 406
	db.session.commit()
	
	familyBudget_json = {}
	
	familyBudget_json['id'] = familyBudget.id
	familyBudget_json['money_amount'] = familyBudget.money_amount
	familyBudget_json['members'] = request.json['member_ids']
	
	return jsonify(familyBudget_json), 200
	
@FamilyBudgets_blueprint.route('/<int:familyBudget_id>', methods=['GET'])
def get_familyBudget(familyBudget_id):
	familyBudget = db.session.query(models.FamilyBudgets).filter_by(id=familyBudget_id).first()
	if familyBudget is None:
		return jsonify({'error': 'Budget not found'}), 404
		
	members = [int(row.user_id) for row in db.session.query(models.FamilyBudgetsUsers).filter_by(family_budget_id=familyBudget_id).all()]
	
	familyBudget_json = {}
	
	familyBudget_json['id'] = familyBudget.id
	familyBudget_json['money_amount'] = familyBudget.money_amount
	familyBudget_json['members'] = members
	
	return jsonify(familyBudget_json), 200
	
		
@FamilyBudgets_blueprint.route('/<int:familyBudgets_id>', methods=['DELETE'])
def delete_familyBudget(familyBudgets_id):
	familyBudget = db.session.query(models.FamilyBudgets).filter_by(id=familyBudgets_id).first()
	if familyBudget is None:
		return jsonify({'error': 'Family budget not found'}), 404
		
	try:
		db.session.delete(familyBudget)
	except:
		db.session.rollback()
		return jsonify({'error': 'Database error'}), 405

	db.session.commit()
	return jsonify({'message': 'family budget deleted successfully'}), 200
	
@FamilyBudgets_blueprint.route('/<int:familyBudgets_id>/report', methods=['GET'])
def get_familyBudget_report(familyBudgets_id):
	familyBudget = db.session.query(models.FamilyBudgets).filter_by(id=familyBudgets_id).first()
	if familyBudget is None:
		return jsonify({'error': 'Budget not found'}), 404
		
	report1 = db.session.query(models.Operation).filter(models.Operation.sender_id==familyBudgets_id and models.Operation.sender_type=="family").all()
	report2 = db.session.query(models.Operation).filter(models.Operation.receiver_id==familyBudgets_id and models.Operation.receiver_type=="family").all()
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
	
@FamilyBudgets_blueprint.route('/<int:familyBudgets_id>/transfer', methods=['POST'])
def post_familyBudget_transfer(familyBudgets_id):
	familyBudget = db.session.query(models.FamilyBudgets).filter_by(id=familyBudgets_id).first()
	if familyBudget is None:
		return jsonify({'error': 'Family budget not found'}), 404
		
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
	
	if familyBudget.money_amount < request.json['money_amount']:
		return jsonify({'error': 'Not enough money'}), 406
	
	now = datetime.now()
	operation = models.Operation(sender_id=familyBudgets_id, receiver_id=request.json['receiver_budget_id'], sender_type="personal", receiver_type=request.json['receiver_type'],money_amount=request.json['money_amount'],date=now)
	
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
		
	familyBudget.money_amount = familyBudget.money_amount - request.json['money_amount']
		
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
		
		
		

