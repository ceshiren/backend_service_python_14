import json

from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_restful import Resource, Api
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
# done: 输出中文
app.config["JSON_AS_ASCII"] = False

api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://python14:python14@stuq.ceshiren.com:23306/python14'
db = SQLAlchemy(app)
# token管理
app.config['JWT_SECRET_KEY'] = 'ceshiren.com'  # Change this!
jwt = JWTManager(app)


class User(db.Model):
    __tablename__ = "seveniruby_user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username


class TestCase(db.Model):
    __tablename__ = "seveniruby_testcase"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(500), unique=False, nullable=False)
    data = db.Column(db.String(1024), unique=False, nullable=False)

    def __repr__(self):
        return '<TestCase %r>' % self.name


class TestCaseApi(Resource):
    @jwt_required
    def get(self):
        r = []
        for t in TestCase.query.all():
            res = {}
            res['id'] = t.id
            res['name'] = t.name
            res['description'] = t.description
            res['data'] = t.data
            r.append(res)
        return r

    @jwt_required
    def post(self):
        t = TestCase(
            name=request.json['name'],
            description=request.json['description'],
            data=request.json['data']
        )
        db.session.add(t)
        db.session.commit()
        return {
            'msg': 'ok'
        }

    @jwt_required
    def put(self):
        pass

    @jwt_required
    def delete(self):
        pass


class LoginApi(Resource):
    def get(self):
        User.query.all()
        return {'hello': 'world'}

    def post(self):
        # done: 查询数据库
        username = request.json.get('username', None)
        # todo: 通常密码不建议原文存储
        password = request.json.get('password', None)
        user = User.query.filter_by(username=username, password=password).first()
        # done：生成返回结构体
        if user is None:

            return jsonify(
                errcode=1,
                errmsg='用户名或者密码不对'
            )
        else:
            # done: 生成token
            return {
                'errcode': 0,
                'errmsg': 'ok',
                'username': user.username,
                'token': create_access_token(identity=user.username)
            }


api.add_resource(TestCaseApi, '/testcase')
api.add_resource(LoginApi, '/login')

if __name__ == '__main__':
    app.run(debug=True)
