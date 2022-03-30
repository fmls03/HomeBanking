from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import *

from home import *

secret_key = str(os.urandom(256))

app = Flask(__name__)
app.config['SECRET_KEY']= secret_key
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://fmlspi:Schipilliti03!@93.51.26.126/HomeBanking'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)

app.register_blueprint(home_bp)



if __name__ == '__main__':
    app.run('localhost', 5000, debug=True)