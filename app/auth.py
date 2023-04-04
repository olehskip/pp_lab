from flask import Flask
from flask_httpauth import HTTPBasicAuth
import app.db as db
from flask_bcrypt import Bcrypt
import app.models as models

# app = Flask(__name__)
auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username, password):
	user = db.session.query(models.Users).filter(models.Users.username==username).first()
	print("user.password")
	print(password)
	print(user.password)
	if user is not None and Bcrypt().check_password_hash(user.password, password):
		return user
	
	return None
