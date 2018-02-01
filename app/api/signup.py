#coding: utf-8
from . import api
from app import db
from flask import request, jsonify, Response
from flask_login import login_user, logout_user, current_user, login_required
from app.models import User
import json

@api.route('/signup/', methods = ['POST'])
def signup():
    if request.method == 'POST':
        username = request.get_json().get('username')
        password = request.get_json().get('password')
        if not User.query.filter_by(username = username).first():
            user = User(username = username,
                        password = password)
            db.session.add(user)
            db.session.commit()
            token = user.generate_confirmation_token()
            return jsonify({
                "uid":user.id,
                "token":token
            })
        else:
            return jsonify({
                "message":"Has already been registered"
            }),400
