from flask import Flask
import config
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config.from_object(config.Config)
Bootstrap(app)

from app import routes
