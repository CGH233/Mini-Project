#coding:utf-8
from flask import jsonify, request, Response
from . import api
from app import db
from app.models import User, Story, Storyc
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
        keyword = []
        sid = []
        for x in storys:
            sid.append(x.id)
            if x.id == storyid:
                uid = x.user_id
                user = User.query.filter_by(id=uid).first()
                username = user.username
                story = x.story
                keywords = x.keywords
                p = []
                scl = []
                for a in keywords.split("&",7):
                    p.append({'keyword':a})  
                likenum = x.likenum
                for sc in storycs:
                    if sc.story_id == storyid:
                        scl.append(sc.id)
                        scl.sort()
                for z in scl:
                    storyc1 = Storyc.query.filter_by(id=z).first()
                    usernamec = User.query.filter_by(id=storyc1.user_id).first().username
                    storyc.append({'storyc':storyc1.storyc,
                                           'usernamec':usernamec})
                return jsonify({"story":story,
                                "likenum":likenum,
                                "username":username,
                                "keywords":p,
                                "storyc":storyc}),200
        if (storyid  in sid) == False:
                return jsonify({
                        "message":"wrong"
                    })

@api.route('/story/<int:storyid>/like/', methods = ['GET'])
def like(storyid):
    if request.method == 'GET':        
        story = Story.query.filter_by(id=storyid).first()
        user = User.query.filter_by(id=story.user_id).first()
        likenum = int(story.likenum) + 1
        userlikenum = int(user.userlikenum) + 1
        story.likenum = likenum
        user.userlikenum = userlikenum
        db.session.add(story,user)
        db.session.commit()
        return jsonify({
            "likenum":story.likenum    
        }),200


@api.route('/story/random/', methods = ['GET'])
def randomstory():
    story = []
    y = []
    if request.method == 'GET':
        x = db.session.query(func.max(Story.id)).scalar()
        a = 0
        while int(a) < 6:
            b = random.randint(1,x)
            if b in y:
                pass
            else:
                a += 1
                y.append(b)
                st = Story.query.all()
                sid = []
                for z in st:
                    sid.append(z.id)
                if b in sid:
                    s = Story.query.filter_by(id=b).first()
                    if len(s.story) > 30:
                           k = s.story[0:30]
                    else:
                           k = s.story
                    username = User.query.filter_by(id=s.user_id).first().username
                    p = []
                    for l in s.keywords.split("&",7):
                        p.append({'keyword':l})
                    story.append({'username':username,
                              'storyid':s.id,
                              'story':k,
                              'likenum':s.likenum,
                              'keyword':p})
        return jsonify({
                    "story":story    
                }),200

@api.route('/story/rank/', methods = ['GET'])
def rank():
    if request.method == 'GET':
        story1 = Story.query.all()
        story = []
        s = []
        b = 0
        for a in story1:
            s.append(a.likenum)
        s.sort()
        for a in range(3):
            n = s[-(a + 1)]
            sn = Story.query.filter_by(likenum=n).first()
            if len(sn.story) > 50:
                k = sn.story[0:50]
            else:
                k = sn.story
            username = User.query.filter_by(id=sn.user_id).first().username
            p = []
            for x in sn.keywords.split("&",7):
                p.append({'keyword':x})
            story.append({'username':username,
                           'storyid':sn.id,
                           'story':k,
                           'likenum':n,
                           'keyword':p})
        return jsonify({
            "rank":story
            }),200                   
	
@api.route('/story/write/', methods = ['POST'])
def write():
    if request.method == 'POST':
        token = request.headers['token']
        uid = request.get_json().get('uid')
        user = User.query.filter_by(id=uid).first()
        if user.confirm(token):
            story = request.get_json().get('story')
            user.userwords += len(story)
            keyword1 = request.get_json().get('keyword')
            c = '&'
            keyword = ''
            for key in keyword1:
                a = keyword1[key] 
                keyword += (a + c)
            likenum = 0
            user.usb += 1
            user.usa += 1
            story1 = Story(story = story,
                            user_id = uid,
                            likenum = likenum,
                            keywords = keyword)
            db.session.add(story1,user)
            db.session.commit()
            return jsonify({
                "storyid":story1.id    
            }),200


@api.route('/story/<int:storyid>/continue/', methods = ['POST'])
def continue1(storyid):
    if request.method == 'POST':
        token = request.headers['token']
        uid = request.get_json().get('uid')
        user = User.query.filter_by(id=uid).first()
        if user.confirm(token):
            storyc = request.get_json().get('storyc')
            story = Story.query.filter_by(id=storyid).first()
            storyc1 = Storyc(storyc=storyc,
                             story_id=storyid,
                             user_id=uid)
            user.usa += 1
            user.userwords += len(storyc)
            db.session.add(storyc1,user)
            db.session.commit()
            return jsonify({
                    "storycid":storyc1.id
                })

@api.route('/story/<int:storyid>/delete/', methods = ['DELETE'])
def delete1(storyid):    
    if request.method == 'DELETE':
        token = request.headers['token']
        story = Story.query.filter_by(id=storyid).first()
        user = User.query.filter_by(id=story.user_id).first()
        if user.confirm(token):
            try:
                storyc = Storyc.query.filter_by(story_id=storyid).first()
            except:
                storyc = None
            if storyc is not None:
                return jsonify({
                            "message":"wrong"
                        }),403
            else:
                db.session.delete(story)
                db.session.commit()
                return jsonify({
                        "message":"OK"
                    }),200
