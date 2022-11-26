echo "is_testing = True" > app/config.py
coverage run --source=app -m pytest tests && coverage report -m
