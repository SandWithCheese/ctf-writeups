import os
import re
from flask import session
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(10), nullable=False)

class Invitation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    code = db.Column(db.String(100), unique=True)

class Vault(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    filename = db.Column(db.String(80), unique=True, nullable=False)


class Database:
    def __init__(self, app=None):
        if app is not None:
            db.init_app(app)
            self.app = app
    
    def is_valid_username(self, username):
        return bool(re.match(r'^[A-Za-z0-9]+$', username))

    def migrate(self, username, password, email, role):
        with self.app.app_context():
            db.drop_all()
            db.create_all()

            print("Admin Password:", password)

            user = User(username=username, password=password, email=email, role=role)
            db.session.add(user)
            db.session.commit()
            
            return user

    def register(self, username, password, email, role, code):
        user = db.session.query(User).filter((User.username == username)).first()
        if user:
            return False, "A user with this username already exists."
        
        invitation = db.session.query(Invitation).filter((Invitation.username == username)).first()

        if invitation == None or invitation.code != code:
            return False, "Invalid invitation code for the given username. Please check and try again."

        user = User(username=username, password=password, email=email, role=role)
        db.session.add(user)
        db.session.commit()
        
        return True, user
    
    def login(self, username, password):
        user = db.session.query(User).filter((User.username == username)).first()
        
        if not user:
            return None

        if user.password != password:
            return None

        return user
            
    def list_invitation(self, username=""):
        if username:
            invitation = db.session.query(Invitation).filter((Invitation.username == username)).first()
        else:
            invitation = db.session.query(Invitation).all()

        return invitation

    def create_invitation(self, username):
        if not self.is_valid_username(username):
            return False, "Username must contain only letters and numbers (A-Z, a-z, 0-9)."

        code = os.urandom(50).hex()
        invitation = db.session.query(Invitation).filter((Invitation.username == username)).first()

        if invitation:
            invitation.code = code
        else:
            invitation = Invitation(username=username, code=code)
            db.session.add(invitation)
        
        db.session.commit()

        return True, "Invite code successfully created"

    def add_image(self, username, filename):
        image = Vault(username=username, filename=filename)
        db.session.add(image)
        db.session.commit()

        return image

    def list_image(self, username):
        return db.session.query(Vault).filter((Vault.username == username)).all()

    def list_users(self):
        return db.session.query(User).all()