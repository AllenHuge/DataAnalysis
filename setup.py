from flask import Flask,render_template,request
from flask_restful import reqparse, abort, Api, Resource
from view import Users
from stock_sh.analy_up_down import Analy_up_down
from stock_sh.query_quot import Query_k_line
from common.db_operation import mysql_login
import pandas as pd
import time
import uuid

# Flask相关变量声明
app = Flask(__name__)
api = Api(app)

TODOS = {
    'todo1': {'task': 'build an API'},
    'todo2': {'task': '哈哈哈'},
    'todo3': {'task': 'profit!'},
}


def abort_if_todo_doesnt_exist(todo_id):
    if todo_id not in TODOS:
        abort(404, message="Todo {} doesn't exist".format(todo_id))


# RESTfulAPI的参数解析 -- put / post参数解析
parser = reqparse.RequestParser()
parser.add_argument('task')


# # 操作（put / get / delete）单一资源Todo
# shows a single todo item and lets you delete a todo item
class Todo(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        return TODOS[todo_id]

    def delete(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        del TODOS[todo_id]
        return '', 204

    def put(self, todo_id):
        args = parser.parse_args()
        task = {'task': args['task']}
        TODOS[todo_id] = task
        return task, 201


# # 操作（post / get）资源列表TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        todo_id = int(max(TODOS.keys()).lstrip('todo')) + 1
        todo_id = 'todo%i' % todo_id
        TODOS[todo_id] = {'task': args['task']}
        return TODOS[todo_id], 201

#获取每日涨跌幅信息
def get_quot(start_date,end_date,code):
    sql = '''
    SELECT
				trade_date
				,index_code
    			,index_name
    			,open_price
    			,high_price
    			,low_price
    			,close_price
	FROM        ext_data_stock.index_quotation_info
    WHERE       trade_date BETWEEN '{0}' AND '{1}' 
    AND         index_code = '{2}'
    '''.format(start_date, end_date, code)

    conn = mysql_login()
    cursor = conn.cursor()
    try:
        cursor.execute(sql)
        data = cursor.fetchall()
    except:
        data = False
        conn.rollback()
    conn.close()
    return data

# 首页,将mysql中表的值读出并传到网页----查
@app.route ('/',methods=["GET","POST"])
def index():
    start_time = time.time()
    flowid = str(uuid.uuid1())  # 查询唯一uid
    result = {
        'success': True,
        'code': 0,
        'message': None,
        'flowId': flowid,
        'time': 0,
        'value': {'flowId': str(flowid), 'ch_colnames': [], 'rows': ()}
    }
    getDicts_raw = request.get_json()
    # start_date = getDicts_raw.get('start_date')
    # end_date = getDicts_raw.get('end_date')
    # code = getDicts_raw.get('code')
    start_date, end_date, code = '2020-01-01', '2020-02-27', 'sh.000001'
    data = get_quot(start_date, end_date, code)
    end_time = time.time()
    ch_colnames = ['日期', '股票代码', '股票名称', '开盘价', '最高价', '最低价', '收盘价']
    result.update({
        'success': True,
        'code': 200,
        'message': '查询成功',
        'flowId': flowid,
        'time': (end_time - start_time) * 1000,
        'value': {'flowId': str(flowid), 'ch_colnames': ch_colnames, 'rows': data}
    })
    return render_template('query.html', datalist=data)


# 设置路由
api.add_resource(TodoList, '/todos')
api.add_resource(Todo, '/todos/<todo_id>')
api.add_resource(Users, "/users")
api.add_resource(Analy_up_down, "/analy_up_down")
api.add_resource(Query_k_line, "/query_k_line")

if __name__ == '__main__':
    # app.run(debug=True, host='127.0.0.1', port=5000)
    app.run(debug=True, host='172.22.193.42', port=5000)