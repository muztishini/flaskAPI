from flask_restful import Resource
from flask import request
from models import Task, db


class TaskList(Resource):
    def get(self):
        tasks = db.session.query(Task).all()
        task_list = [{'id': task.id, 'description': task.description}
                     for task in tasks]
        return {'tasks': task_list}

    def post(self):
        task_data = request.get_json()
        if not task_data:
            return {'message': 'No input data provided'}, 400
        description = task_data.get('description')
        if not description:
            return {'message': 'Description is required'}, 400
        new_task = Task(description=description)
        db.session.add(new_task)
        db.session.commit()
        return {'message': 'Task added', 'task': {'id': new_task.id, 'description': new_task.description}}


class TaskApi(Resource):
    def get(self, task_id):
        task = db.session.query(Task).get(task_id)
        if task:
            return {'id': task.id, 'description': task.description}
        else:
            return {'message': 'Task not found'}

    def put(self, task_id):
        task = db.session.query(Task).get(task_id)
        if task:
            task_data = request.get_json()
            description = task_data.get('description')
            if not description:
                return {'message': 'Description is required'}, 400
            task.description = description
            db.session.commit()
            return {'message': 'Task update', 'task': {'id': task.id, 'description': task.description}}
        else:
            return {"message": "Task not found"}

    def delete(self, task_id):
        task = db.session.query(Task).get(task_id)
        if task:
            db.session.delete(task)
            db.session.commit()
            return {'message': f"Task {task_id} deleted"}
        else:
            return {"message": "Task not found"}
