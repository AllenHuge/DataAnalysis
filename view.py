from flask import render_template, Flask

app = Flask(__name__)

#创建路由
@app.route('/')
def homepage():
    return render_template("000001SH.html") #templates文件夹下