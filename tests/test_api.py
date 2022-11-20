import json
import base64
import app.models as models
import app.db as db
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

def test_create_user(client):
    response = client.post(
        'user',
        content_type='application/json',
        data=json.dumps({
            'surname': 'Test',
            'name': 'Test',
            'username': 'Test',
            'password': 'Test'
        }))       
    assert response.status_code == 201 

def test_create_family_budget(client):
    valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
    response = client.post(
        'family_budget/',
        headers={'Authorization': 'Basic ' + valid_credentials},
        content_type='application/json',
        data=json.dumps({
            'members_ids': []
        })
    )
    assert response.status_code == 200


class Test_PersonalBudget:

    # Get personal budget

    def test_get_personal_budget(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.get(
            'personal_budget/1',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json'
        )
        assert response.status_code == 200

    def test_403_get_personal_budget(self, client):
        user = models.Users(surname='Test2', name='Test2', username='Test2', password=bcrypt.generate_password_hash('Test2').decode('utf-8'))
        db.session.add(user)
        db.session.commit()
        valid_credentials = base64.b64encode(b"Test2:Test2").decode("utf-8")
        response = client.get(
            'personal_budget/1',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json'
        )
        assert response.status_code == 403

    def test_401_get_personal_budget(self, client):
        valid_credentials = base64.b64encode(b"Test1:Test1").decode("utf-8")
        response = client.get(
            'personal_budget/1',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json'
        )
        assert response.status_code == 401

    # Post personal budget transfer

    def test_post_personal_budget_transfer(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.post(
            'personal_budget/1/transfer',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
            data=json.dumps({
                'receiver_budget_id': 1,
                'receiver_type': 'personal',
                'money_amount': 2
            })
        )
        assert response.status_code == 200

    def test_2_post_personal_budget_transfer(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.post(
            'personal_budget/1/transfer',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
            data=json.dumps({
                'receiver_budget_id': 1,
                'receiver_type': 'family',
                'money_amount': 2
            })
        )
        assert response.status_code == 200

    def test_403_post_personal_budget_transfer(self, client):
        valid_credentials = base64.b64encode(b"Test2:Test2").decode("utf-8")
        response = client.post(
            'personal_budget/1/transfer',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
            data=json.dumps({
                'receiver_budget_id': 1,
                'receiver_type': 'personal',
                'money_amount': 10
            })
        )
        assert response.status_code == 403

    def test_401_post_personal_budget_transfer(self, client):
        valid_credentials = base64.b64encode(b"Test1:Test1").decode("utf-8")
        response = client.post(
            'personal_budget/1/transfer',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
            data=json.dumps({
                'receiver_budget_id': 1,
                'receiver_type': 'personal',
                'money_amount': 10
            })
        )
        assert response.status_code == 401

    def test_400_post_personal_budget_transfer(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.post(
            'personal_budget/1/transfer',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
            data=json.dumps({
                'receiver_budget_id': 1,
                'receiver_type': 'personal',
                'money_amount': 100
            })
        )
        assert response.status_code == 400

    def test_400_2_post_personal_budget_transfer(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.post(
            'personal_budget/1/transfer',
            headers={'Authorization': 'Basic ' + valid_credentials},
        )
        assert response.status_code == 400

    def test_400_3_post_personal_budget_transfer(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.post(
            'personal_budget/1/transfer',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
            data=json.dumps({
                'wrong': 'wrong'
            })
        )
        assert response.status_code == 400

    def test_400_4_post_personal_budget_transfer(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.post(
            'personal_budget/1/transfer',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
            data=json.dumps({
                'receiver_budget_id': 1,
                'receiver_type': 'personal',
                'money_amount': 0
            })
        )
        assert response.status_code == 400

    def test_400_5_post_personal_budget_transfer(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.post(
            'personal_budget/1/transfer',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
            data=json.dumps({
                'receiver_budget_id': 1,
                'receiver_type': 'personal',
                'money_amount': 100000
            })
        )
        assert response.status_code == 400

    def test_408_post_personal_budget_transfer(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.post(
            'personal_budget/1/transfer',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
            data=json.dumps({
                'receiver_budget_id': 26,
                'receiver_type': 'personal',
                'money_amount': 2
            })
        )
        print(response.data)
        assert response.status_code == 408

    def test_408_2_post_personal_budget_transfer(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.post(
            'personal_budget/1/transfer',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
            data=json.dumps({
                'receiver_budget_id': 26,
                'receiver_type': 'family',
                'money_amount': 2
            })
        )
        print(response.data)
        assert response.status_code == 408

    # Get personal budget report

    def test_get_personal_budget_report(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.get(
            'personal_budget/1/report',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json'
        )
        assert response.status_code == 200

    def test_403_get_personal_budget_report(self, client):
        valid_credentials = base64.b64encode(b"Test2:Test2").decode("utf-8")
        response = client.get(
            'personal_budget/1/report',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json'
        )
        assert response.status_code == 403

    def test_401_get_personal_budget_report(self, client):
        valid_credentials = base64.b64encode(b"Test1:Test1").decode("utf-8")
        response = client.get(
            'personal_budget/1/report',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json'
        )
        assert response.status_code == 401


class Test_FamilyBudget:

# Create family budget

    def test_401_create_family_budget(self, client):
        valid_credentials = base64.b64encode(b"Test1:Test1").decode("utf-8")
        response = client.post(
            'family_budget/',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
            data=json.dumps({
                'members_ids': []
            })
        )
        assert response.status_code == 401

    def test_400_2_create_family_budget(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.post(
            'family_budget/',
            headers={'Authorization': 'Basic ' + valid_credentials}
        )
        assert response.status_code == 400

    def test_400_create_family_budget(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.post(
            'family_budget/',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
            data = json.dumps({'wrong': 'data'})
        )
        assert response.status_code == 400

# Get family budget

    def test_get_family_budget(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.get(
            'family_budget/1',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json'
        )
        assert response.status_code == 200

    def test_401_get_family_budget(self, client):
        valid_credentials = base64.b64encode(b"Test1:Test1").decode("utf-8")
        response = client.get(
            'family_budget/1',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json'
        )
        assert response.status_code == 401

    def test_404_get_family_budget(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.get(
            'family_budget/2',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json'
        )
        assert response.status_code == 404

    def test_403_get_family_budget(self, client):
        user = models.Users(surname='Test3', name='Test3', username='Test3', password=bcrypt.generate_password_hash('Test3').decode('utf-8'))
        db.session.add(user)
        db.session.commit()
        valid_credentials = base64.b64encode(b"Test3:Test3").decode("utf-8")
        response = client.get(
            'family_budget/1',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json'
        )
        assert response.status_code == 403

# Get family budget report

    def test_get_family_budget_report(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.get(
            'family_budget/1/report',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json'
        )
        assert response.status_code == 200

    def test_401_get_family_budget_report(self, client):
        valid_credentials = base64.b64encode(b"Test1:Test1").decode("utf-8")
        response = client.get(
            'family_budget/1/report',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json'
        )
        assert response.status_code == 401

    def test_404_get_family_budget_report(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.get(
            'family_budget/2/report',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json'
        )
        assert response.status_code == 404

    def test_403_get_family_budget_report(self, client):
        valid_credentials = base64.b64encode(b"Test3:Test3").decode("utf-8")
        response = client.get(
            'family_budget/1/report',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json'
        )
        assert response.status_code == 403

# Post transfer

    def test_post_family_budget_transfer(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.post(
            'family_budget/1/transfer',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
            data=json.dumps({
                'receiver_budget_id': 1,
                'receiver_type': 'family',
                'money_amount': 2
            })
        )
        assert response.status_code == 200

    def test_2_post_family_budget_transfer(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.post(
            'family_budget/1/transfer',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
            data=json.dumps({
                'receiver_budget_id': 1,
                'receiver_type': 'personal',
                'money_amount': 2
            })
        )
        assert response.status_code == 200

    def test_401_post_family_budget_transfer(self, client):
        valid_credentials = base64.b64encode(b"Test1:Test1").decode("utf-8")
        response = client.post(
            'family_budget/1/transfer',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
            data=json.dumps({
                'receiver_budget_id': 1,
                'receiver_type': 'family',
                'money_amount': 10
            })
        )
        assert response.status_code == 401

    def test_404_post_family_budget_transfer(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.post(
            'family_budget/2/transfer',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
            data=json.dumps({
                'receiver_budget_id': 1,
                'receiver_type': 'family',
                'money_amount': 10
            })
        )
        assert response.status_code == 404

    def test_403_post_family_budget_transfer(self, client):
        valid_credentials = base64.b64encode(b"Test3:Test3").decode("utf-8")
        response = client.post(
            'family_budget/1/transfer',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
            data=json.dumps({
                'receiver_budget_id': 1,
                'receiver_type': 'family',
                'money_amount': 10
            })
        )
        assert response.status_code == 403

    def test_400_post_family_budget_transfer(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.post(
            'family_budget/1/transfer',
            headers={'Authorization': 'Basic ' + valid_credentials},
        )
        assert response.status_code == 400

    def test_400_2_post_family_budget_transfer(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.post(
            'family_budget/1/transfer',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
            data=json.dumps({'wrong': 'data'})
        )
        assert response.status_code == 400

    def test_407_post_family_budget_transfer(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.post(
            'family_budget/1/transfer',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
            data=json.dumps({
                'receiver_budget_id': 1,
                'receiver_type': 'family',
                'money_amount': 0
            })
        )
        assert response.status_code == 407

    def test_406_post_family_budget_transfer(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.post(
            'family_budget/1/transfer',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
            data=json.dumps({
                'receiver_budget_id': 1,
                'receiver_type': 'family',
                'money_amount': 11110
            })
        )
        assert response.status_code == 406

    def test_408_post_family_budget_transfer(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.post(
            'family_budget/1/transfer',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
            data=json.dumps({
                'receiver_budget_id': 2,
                'receiver_type': 'family',
                'money_amount': 2
            })
        )
        assert response.status_code == 408

    def test_408_2_post_family_budget_transfer(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.post(
            'family_budget/1/transfer',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
            data=json.dumps({
                'receiver_budget_id': 2,
                'receiver_type': 'personal',
                'money_amount': 2
            })
        )
        assert response.status_code == 408

# Delete family budget

    def test_401_delete_family_budget(self, client):
        valid_credentials = base64.b64encode(b"Test1:Test1").decode("utf-8")
        response = client.delete(
            'family_budget/1',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
        )
        assert response.status_code == 401

    def test_404_delete_family_budget(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.delete(
            'family_budget/2',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
        )
        assert response.status_code == 404

    def test_403_delete_family_budget(self, client):
        valid_credentials = base64.b64encode(b"Test3:Test3").decode("utf-8")
        response = client.delete(
            'family_budget/1',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
        )
        assert response.status_code == 403

    def test_delete_family_budget(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.delete(
            'family_budget/1',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
        )
        assert response.status_code == 200


class Test_User:

    # Create user

    def test_400_create_user(self, client):
        response = client.post(
            'user',
            content_type='application/json',
            data=json.dumps({
                'wrong': 'wrong'
            }))       
        assert response.status_code == 400 

    def test_400_2_create_user(self, client):
        response = client.post(
            'user'
        )
        assert response.status_code == 400 

    def test_401_create_user(self, client):
        response = client.post(
            'user',
            content_type='application/json',
            data=json.dumps({
                'surname': 'Test',
                'name': 'Test',
                'username': 'Test',
                'password': 'Test'
            }))       
        assert response.status_code == 401 

    # Get user
    
    def test_get_user(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.get(
            'user/1', 
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json'
        )
        assert response.status_code == 200

    def test_401_get_user(self, client):
        valid_credentials = base64.b64encode(b"Test123:Test123").decode("utf-8")
        response = client.get(
            'user/1', 
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json'
        )
        assert response.status_code == 401

    def test_404_get_user(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.get(
            'user/10', 
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json'
        )
        assert response.status_code == 404

    def test_403_get_user(self, client):
        user = models.Users(surname='Test4', name='Test4', username='Test4', password=bcrypt.generate_password_hash('Test4').decode('utf-8'))
        db.session.add(user)
        db.session.commit()
        valid_credentials = base64.b64encode(b"Test4:Test4").decode("utf-8")
        response = client.get(
            'user/1', 
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json'
        )
        assert response.status_code == 403

    # Update user

    def test_update_user(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.patch(
            'user/1',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
            data=json.dumps({
                'surname': 'Test'
        }))
        assert response.status_code == 200

    def test_2_update_user(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.patch(
            'user/1',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
            data=json.dumps({
                'name': 'Test'
        }))
        assert response.status_code == 200

    def test_3_update_user(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.patch(
            'user/1',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
            data=json.dumps({
                'username': 'Test'
        }))
        assert response.status_code == 200

    def test_4_update_user(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.patch(
            'user/1',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
            data=json.dumps({
                'password': 'Test'
        }))
        assert response.status_code == 200

    def test_400_update_user(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.patch(
            'user/1',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
            data=json.dumps({
                'wrong': 'wrong'
        }))
        assert response.status_code == 400

    def test_400_2_update_user(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.patch(
            'user/1',
            headers={'Authorization': 'Basic ' + valid_credentials}
        )
        assert response.status_code == 400

    def test_401_update_user(self, client):
        valid_credentials = base64.b64encode(b"Test123:Test123").decode("utf-8")
        response = client.patch(
            'user/1',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
            data=json.dumps({
                'surname': 'Test'
        }))
        assert response.status_code == 401

    def test_403_update_user(self, client):
        valid_credentials = base64.b64encode(b"Test4:Test4").decode("utf-8")
        response = client.patch(
            'user/1',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
            data=json.dumps({
                'surname': 'Test'
        }))
        assert response.status_code == 403

    def test_404_update_user(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.patch(
            'user/10',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
            data=json.dumps({
                'surname': 'Test'
        }))
        assert response.status_code == 404

    # Delete user

    def test_401_delete_user(self, client):
        valid_credentials = base64.b64encode(b"Test123:Test123").decode("utf-8")
        response = client.delete(
            'user/1',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
        )
        assert response.status_code == 401

    def test_404_delete_user(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.delete(
            'user/10',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
        )
        assert response.status_code == 404

    def test_403_delete_user(self, client):
        valid_credentials = base64.b64encode(b"Test4:Test4").decode("utf-8")
        response = client.delete(
            'user/1',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
        )
        assert response.status_code == 403

    def test_delete_user(self, client):
        valid_credentials = base64.b64encode(b"Test:Test").decode("utf-8")
        response = client.delete(
            'user/1',
            headers={'Authorization': 'Basic ' + valid_credentials},
            content_type='application/json',
        )
        assert response.status_code == 200
