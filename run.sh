echo "is_testing = False" > config.py
gunicorn -w 2 -b 0.0.0.0:5000 app:app
