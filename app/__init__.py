from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_cors import CORS
from dotenv import load_dotenv
load_dotenv()
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)




app.config['SECRET_KEY'] = 'super secret key'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config["SQLALCHEMY_DATABASE_URI"]= os.environ.get("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]= True
 




CORS(app)

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'mydatabase.db')
db = SQLAlchemy(app)

app.config.from_object(__name__)
from app import views
