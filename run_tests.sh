echo "is_testing = True" > config.py
coverage run --source=app -m pytest tests && coverage report -m
