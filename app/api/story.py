#coding:utf-8
from flask import jsonify, request, Response
from . import api
from app import db
from app.models import User, Story, Storyc, Keyword
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy.sql import func
import random
import json

@api.route('/story/<int:storyid>/', methods = ['GET'])
def readstory(storyid):
    if request.method == 'GET':
        storys = Story.query.all()
        storycs = Storyc.query.all()
        storyc = []
        usernamec = []

        for x in storys:
            s = Story.query.filter_by(story=x.story).first()
            if int(s.id) == storyid:
                uid = s.user_id
                user = User.query.filter_by(id=uid).first()
                username = user.username
                story = s.story
                likenum = s.likenum
                for sc in storycs:
                    if sc.story_id == storyid:
                        storyc.append(sc.storyc)      
                        usernamec.append(User.query.filter_by(id=sc.user_id).first())
                return jsonify({
                    "story":story,
                    "likenum":likenum,
                    "username":username,
                    "storyc":[{
                        "storyc":storyc,
                        "usernamec":usernamec
                    }]
                }),200

@api.route('/story/<int:storyid>/like/', methods = ['GET'])
def like(storyid):
    if request.method == 'GET':
        
        story = Story.query.filter_by(id=storyid).first()
        likenum = story.likenum + 1
        return jsonify({
            "likenum":likenum    
        }),200


@api.route('/story/random/', methods = ['GET'])
def randomstory():
    a = 0
    story = []
    username = []
    storyid = []
    likenum = []
    keyworda = []
    keyword = []
    if request.method == 'GET':
        x = Story.query(func.max(Story.id)).all()
        while a<5:
            a += 1
            s = Story.query.filter_by(id=random(1,x))
            k = Keyword.query.filter_by(story_id=s.id)
            story.append(s.story[0:27]+'...')
            username.append(User.query.filter_by(id=s.user_id).first().username)
            likenum.append(s.likenum)
            storyid.append(s.id)
            keyworda.append(keyword.append(k.keyword1,
                           k.keyword2,
                           k.keyword3,
                           k.keyword4,
                           k.keyword5,                          
                           k.keyword6,     
                           k.keyword7,
                           k.keyword8)
                           )
            return jsonify({
            "story":[{
                "username":username,
                "storyid":storyid,
                "story":story,
                "likenum":likenum,
                "keyword":keyworda
            }]    
        }),200

@api.route('/story/rank/', methods = ['GET'])
def rank():
    if request.method == 'GET':
        story = Story.query.all()
        story3 = []
        username = []
        storyid = []
        likenum = []
        keyworda = []
        keyword = []
        s = []
        b = 0
        for a in story:
            s.append(a.likenum)
        s.sort()
        for x in range(3):
            x = x + 1
            n = s[-x]
            sn = Story.query.filter_by(likenum=n).first()
            story3.append(sn.story[0:47]+'...')
            username.append(User.query.filter_by(id=sn.user_id).username)
            storyid.append(sn.id)
            likenum.append(n)
            keyworda.append(keyword.append(k.keyword1,
            		                   k.keyword2,
                           		   k.keyword3,
                         		   k.keyword4,
                          	 	   k.keyword5,                    
                           		   k.keyword6,     
                           		   k.keyword7,
                           		   k.keyword8))
            return jsonify({
                "story":[{
                    "username":username,
                    "storyid":storyid,
                    "story":story3,
                    "likenum":likenum,
                    "picture":picture,
                    "keyword":keyworda
                    }]
            }),200                   
	
@api.route('/story/write/', methods = ['POST'])
def write():
    if request.method == 'POST':
        token = request.headers['token']
        uid = request.get_json().get('uid')
        user1 = User.query.filter_by(id=uid).first()
        if user1.confirm(token):
            story = request.get_json().get('story')
            storys = Story.query.all()
            for x in storys:
                keyword1 = request.get_json().get('keyword')
                story1 = Story(story = story,
                               user_id = uid)
                keyword = Keyword(keyword1 = keyword1[0],
                      keyword2 = keyword1[1],
                      keyword3 = keyword1[2],
                      keyword4 = keyword1[3],
                      keyword5 = keyword1[4],
                      keyword6 = keyword1[5],
                      keyword7 = keyword1[6],
                      keyword8 = keyword1[7])
                db.session.add(story1,keyword)
                db.session.commit()
                return jsonify({
                    "storyid":story1.id    
                }),200
