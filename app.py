from flask import Flask
from flask_restful import Api
from models import db
from resources import TaskList, TaskApi

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
db.init_app(app)
api = Api(app)

api.add_resource(TaskList, '/tasks', endpoint='tasks')
api.add_resource(TaskApi, '/task/<int:task_id>', endpoint='task')

if __name__ == "__main__":
    # with app.app_context():
    #     db.create_all()
    app.run(debug=True)
