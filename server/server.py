import os
from uuid import uuid4
from flask import Flask, jsonify, request, Response
from flask_cors import CORS
import os
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import datetime
import bcrypt
import json
from werkzeug.datastructures.file_storage import FileStorage



app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('HR_SERVER_CONNECTION_STRING') or 'mysql+pymysql://root:toor@localhost/app'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'
db = SQLAlchemy(app)

ma=Marshmallow(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(200))
    login = db.Column(db.String(300))
    password_hash = db.Column(db.String(1000))
    def __init__(self, login, name, password):
        self.login = login
        self.name = name
        self.password_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())



class UserSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'login')

class Submission(db.Model):
    __tablename__ = 'submissions'
    id = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer)
    video_id = db.Column(db.String(600))
    result = db.Column(db.JSON, nullable=True)
    status = db.Column(db.Integer)
    submitted_at = db.Column(db.DateTime, default=datetime.datetime.now)
    def __init__(self, user_id, video: FileStorage):
        if video.filename != '':
            video_id = uuid4(video.filename).hex
            video.save(video_id)
        self.user_id = user_id
        self.video_id = video_id
        self.status = 0


class SubmissionSchema(ma.Schema):
    class Meta:
        fields = ('id', 'user_id', 'video_id', 'result', 'status', 'submitted_at')

user_schema = UserSchema()
users_schema = UserSchema(many=True)
submission_schema = SubmissionSchema()
submissions_schema = SubmissionSchema(many=True)

@app.route('/get',methods=['GET'])
def get_users():
    all_users = User.query.all()
    results = users_schema.dump(all_users)
    print(results)
    return jsonify(results)

@app.route('/user/create', methods=['PUT'])
def create_user():
    try:
        user = User(request.json['login'], request.json['name'], request.json['password'])
        db.session.add(user)
        db.session.commit()
        return user_schema.jsonify(user)
    except Exception as e:
        return jsonify({'error': str(e)}), 409

@app.route('/submission/create', methods=['PUT'])
def create_submission():
    # AUTH
    try:
        js = json.loads(request.form['json'])
        sub = Submission(js['user_id'], request.files['video'])
        db.session.add(sub)
        db.session.commit()
        return submission_schema.jsonify(sub)
    
    except Exception as e:
        return jsonify({'error': str(e)}), 409

if __name__ == '__main__':
    app.run(debug=True)