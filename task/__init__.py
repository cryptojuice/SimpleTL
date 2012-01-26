from flask import Flask
from task import settings
from views.main import main

app = Flask("task")
app.register_blueprint(main)
app.config['SECRET_KEY'] = settings.SECRET_KEY

from models import users

from views import main
