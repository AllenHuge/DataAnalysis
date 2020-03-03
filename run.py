from flask import Flask, jsonify, request, render_template
from flask_restful import reqparse, abort, Resource, Api

from view import Users

app = Flask(__name__)
api = Api(app)

# 创建路由
@app.route('/')
def homepage():
    # templates文件夹下
    return render_template("000001SH.html")


# 设置路由，即路由地址为http://127.0.0.1:5000/users
api.add_resource(Users, "/users")

if __name__ == '__main__':
    # app.run(debug=True,host='127.0.0.1',port=5000)
    app.run(debug=True,host='172.22.193.42',port=5000)