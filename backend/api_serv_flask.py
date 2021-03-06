from flask import Flask
from flask import request
from posgresql_utility import Postgresql
import json
from flask_cors import CORS # <-追加


app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 40845
CORS(app)
psql=Postgresql()

@app.route("/api/post_image", methods=['POST'])
def postImage():
    try:
        param = request.get_json()
        user_id = param.get("user_id")
        image = param.get("image")
        #register data
        sql = "insert into tbl_save_image(user_id,image) values('{0}','{1}');".format(user_id,image)

        psql = Postgresql()
        psql.connection()
        result = psql.sql_exec(sql)
        psql.close()
        print("---end---")
        return {"flag":"0"}, 200

    except Exception as ex:
        psql.close()
        return {"flag":"-1","errorlog":ex}, 200

@app.route("/api/get_image", methods=['GET'])
def getImage():
    try:
        #param = request.get_json()
        #user_id = param.get("user_id")
        user_id = request.args.get("user_id")
        psql = Postgresql()
        psql.connection()
        #get data
        print(user_id)
        sql = "SELECT image FROM tbl_create_image WHERE user_id = '{0}';".format(user_id)
        print(user_id)
        print("1")

        result = psql.sql_exec(sql)
        print("1")
        psql.close()
        print("1")
        print(result)
        image_base64 = "data:image/png;base64,"+result[0][0]
        print("1")
        return {"flag":"0","image":image_base64}, 200
    except Exception as ex:
        psql.close()
        print(ex)
        return {"flag":"-1","errorlog":ex}, 200

@app.route("/")
def hello_world():
  return "Hello, World!", 200


app.run(host="127.0.0.1", port=5000)
