#coding:utf-8
from flask import jsonify, request, Response
from . import api
from app import db
from app.models import User, Story, Storyc
from flask_login import login_user, logout_user, current_user, login_required
import json

@api.route('/user/<int:uid>/', methods = ['GET'])
def me(uid):
    if request.method == 'GET':
        token = request.headers['token']
        user = User.query.filter_by(id=uid).first()
        if user.confirm(token):
            usa = user.usa
            usb = user.usb
            userlikenum = user.userlikenum
            userwords = user.userwords
            return jsonify({"usa":usa,
                            "usb":usb,
                            "userlikenum":userlikenum,
                            "userwords":userwords}),200

@api.route('/user/<int:uid>/join/', methods = ['GET'])
def join(uid):
    if request.method == 'GET':
        token = request.headers['token']
        user = User.query.filter_by(id=uid).first()
        if user.confirm(token):
            story = []
            y = []
            s = Story.query.all()
            for a in s:
                if a.user_id == uid:
                    y.append(a.id)
                    story1 = a.story
                    if len(story1) > 30:
                        s1 = story1[0:30]
                    else:
                        s1 = story1
                    storyid1 = a.id
                    story.append({'story':s1,
                                  'storyid':storyid1})
            sc = Storyc.query.all()
            for b in sc:
                if b.story_id in y:
                    pass
                else:
                    if b.user_id == uid:
                        storyid2 = b.story_id
                        Story2 = Story.query.filter_by(id=storyid2).first()
                        story2 = Story2.story
                        if len(story2) > 30:
                            s2 = story2
                        else:
                            s2 = story2
                        story.append({'story':s2,
                                      'storyid':storyid2})
            return jsonify({"story":story}),200

@api.route('/user/<int:uid>/write/', methods = ['GET'])
def begin(uid):
    if request.method == 'GET':
        token = request.headers['token']
        user = User.query.filter_by(id=uid).first()
        if user.confirm(token):
            story = []
            s = Story.query.all()
            for a in s:
                if a.user_id == uid:
                    story1 = a.story
                    if len(story1) > 30:
                        s1 = story1[0:30]
                    else:
                        s1 = story1
                    storyid1 = a.id
                    story.append({'story':s1,
                                  'storyid':storyid1})
            return jsonify({"story":story}),200
    
