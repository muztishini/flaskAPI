from flask import Flask
from flask_restful import Api
from models import db
from resources import TaskList, TaskApi
import pymysql


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "mysql+pymysql://root:12345@localhost/tasksapi"
db.init_app(app)
api = Api(app)

api.add_resource(TaskList, '/tasks')
api.add_resource(TaskApi, '/tasks/<int:task_id>')

if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)
