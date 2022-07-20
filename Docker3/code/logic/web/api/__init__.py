from enum import unique
from flask import Flask, request
from flask_restful import Api, Resource, reqparse
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
api=Api(app)
app.config.from_object("api.config.Config")
db=SQLAlchemy(app)

class Striver(db.Model):
    __tablename__ = 'strivers'
    id=db.Column(db.Integer, primary_key=True, unique=True)
    email=db.Column(db.String(64), unique=True, nullable=False)
    name=db.Column(db.String(64), unique=False, nullable=True)
    
    def __init__(self, email, name=""):

        self.email=email
        self.name=name


class Striver_api(Resource):
    def get(self):
        # arg_parser = reqparse.RequestParser()
        # arg_parser.add_argument('email', type=str)

        # args=arg_parser.parse_args()
        email_ = request.args['email']

        try:
            #return {'email': email}
            striver_info= db.session.query(Striver).filter_by(email=email_).first()
            return {'Name': striver_info.name,"email": striver_info.email }
        except:
            return {'ERROR': 'Could not insert email'}

        

    def post(self):
        # arg_parser = reqparse.RequestParser()
        # arg_parser.add_argument('email', type=str)
        # arg_parser.add_argument('name', type=str)

        # args=arg_parser.parse_args()
        email_ = request.form['email']
        name_ = request.form['name']
        try:

            db.session.add( Striver(email=email_, name=name_) )
            db.session.commit()

            return {'email': email_, 'name': name_}
        except Exception as exc:
            print(exc) 
            return {'ERROR': 'Could not add email'}
            
api.add_resource(Striver_api, '/striver')