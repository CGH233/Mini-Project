#coding:utf-8
from flask import jsonify, request, Response
from . import api
from app import db
from app.models import User, Story, Storyc
from flask_login import login_user, logout_user, current_user, login_required
import json

@api.route('/story/<int:storyid>/', methods = ['GET'])
def readstory(storyid):
    if request.method == 'GET':
        storys = Story.query.all()
        storycs = Storyc.query.all()
        a = []

        for s in storys:
            if s.id == storyid:
                uid = s.user_id
                user = User.query.filter_by(id=uid),first()
                username = user.username
                story = s.story
                title = s.title
                likenum = s.likenum
                picture = s.picture
                for sc in storycs:
                    if sc.story_id == storyid:
                        a.append(sc.id)
        
    return jsonify({
            "ti"
    })
                
