from marshmallow import Schema, fields, ValidationError
from datetime import datetime
from flask import Blueprint, jsonify, request
import app.models as models
import app.db as db
from flask_bcrypt import Bcrypt
from app.auth import auth

family_budgets_blieprint = Blueprint('FamilyBudgets', __name__, url_prefix='/api/family_budget')
bcrypt = Bcrypt()

@family_budgets_blieprint.route('/', methods=['POST'])
@auth.login_required
def create_new_familyBudget():
    class MembersIds(Schema):
        members_ids = fields.List(fields.Int(), required=True)
        
    try:
        if not request.json:
            raise ValidationError('No input data provided')
        MembersIds().load(request.json)
    except ValidationError as err:
        return jsonify(err.messages), 400
        
    family_budget = models.FamilyBudgets(money_amount=10)
    
    if auth.current_user().id not in request.json['members_ids']:
        request.json['members_ids'].append(auth.current_user().id)

    if len(request.json['members_ids']) < 3:
        return jsonify({'error': 'Family budget must have at least 3 members'}), 400

    for member_id in request.json['members_ids']:
        if db.session.query(models.Users).get(member_id) is None:
            return jsonify({'error': 'User with id {} does not exist'.format(member_id)}), 400

    db.session.add(family_budget)
    db.session.commit()

    for members_ids in request.json['members_ids']:
        family_budget_user = models.FamilyBudgetsUsers(family_budget_id=family_budget.id, user_id=members_ids)
        db.session.add(family_budget_user)
    db.session.commit()

    familyBudget_json = {}
    
    familyBudget_json['id'] = family_budget.id
    familyBudget_json['money_amount'] = family_budget.money_amount
    familyBudget_json['members'] = request.json['members_ids']
    
    
    return jsonify(familyBudget_json), 200
    
@family_budgets_blieprint.route('/<int:family_budget_id>', methods=['GET'])
@auth.login_required
def get_familyBudget(family_budget_id):
    familyBudget = db.session.query(models.FamilyBudgets).filter_by(id=family_budget_id).first()
    if familyBudget is None:
        return jsonify({'error': 'Budget not found'}), 404

    members = [int(row.user_id) for row in db.session.query(models.FamilyBudgetsUsers).filter_by(family_budget_id=models.FamilyBudgetsUsers.family_budget_id).all()]
    if auth.current_user().id not in members:
        return jsonify({'error': 'You are not a member of this budget'}), 403

    familyBudget_json = {}
    
    familyBudget_json['id'] = familyBudget.id
    familyBudget_json['money_amount'] = familyBudget.money_amount
    familyBudget_json['members'] = members
    
    return jsonify(familyBudget_json), 200

@family_budgets_blieprint.route('/<int:family_budget_id>', methods=['DELETE'])
@auth.login_required
def delete_familyBudget(family_budget_id):
    familyBudget = db.session.query(models.FamilyBudgets).filter_by(id=family_budget_id).first()
    if familyBudget is None:
        return jsonify({'error': 'Family budget not found'}), 404
    
    members = [int(row.user_id) for row in db.session.query(models.FamilyBudgetsUsers).filter_by(family_budget_id=family_budget_id).all()]
    if auth.current_user().id not in members:
        return jsonify({'error': 'You are not a member of this budget'}), 403

    db.session.delete(familyBudget)

    db.session.commit()
    return jsonify({'message': 'family budget deleted successfully'}), 200
    
@family_budgets_blieprint.route('/<int:familyBudgets_id>/report', methods=['GET'])
@auth.login_required
def get_familyBudget_report(familyBudgets_id):
    familyBudget = db.session.query(models.FamilyBudgets).filter_by(id=familyBudgets_id).first()
    if familyBudget is None:
        return jsonify({'error': 'Budget not found'}), 404
        
    members = [int(row.user_id) for row in db.session.query(models.FamilyBudgetsUsers).filter_by(family_budget_id=familyBudgets_id).all()]
    if auth.current_user().id not in members:
        return jsonify({'error': 'You are not a member of this budget'}), 403

    report1 = db.session.query(models.Operation).filter(models.Operation.sender_id==familyBudgets_id and models.Operation.sender_type=="family").all()
    report2 = db.session.query(models.Operation).filter(models.Operation.receiver_id==familyBudgets_id and models.Operation.receiver_type=="family").all()
        
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
    
@family_budgets_blieprint.route('/<int:family_budget_id>/transfer', methods=['POST'])
@auth.login_required
def post_familyBudget_transfer(family_budget_id):
    family_budget = db.session.query(models.FamilyBudgets).filter_by(id=family_budget_id).first()
    if family_budget is None:
        return jsonify({'error': 'Family budget not found'}), 404

    members = [int(row.user_id) for row in db.session.query(models.FamilyBudgetsUsers).filter_by(family_budget_id=models.FamilyBudgetsUsers.family_budget_id).all()]
    if auth.current_user().id not in members:
        return jsonify({'error': 'You are not a member of this budget'}), 403
    
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
    
    if family_budget.money_amount < request.json['money_amount']:
        return jsonify({'error': 'Not enough money'}), 400
    
    now = datetime.now()
    operation = models.Operation(sender_id=family_budget_id, receiver_id=request.json['receiver_budget_id'], sender_type="personal", receiver_type=request.json['receiver_type'],money_amount=request.json['money_amount'],date=now)
    
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
        
    family_budget.money_amount = family_budget.money_amount - request.json['money_amount']
        
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
    
