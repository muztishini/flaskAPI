from flask_restful import Resource
from flask import request
# from datetime import datetime
from models import Task, db


class TaskList(Resource):
    def get(self):
        tasks = db.session.query(Task).all()
        task_list = [{'id': task.id, 'title': task.title, 'description': task.description, 'created_at': str(task.created_at),
                    'updated_at': str(task.updated_at)} for task in tasks]
        if task_list:
            return {'tasks': task_list}
        else:
            return {'message': "No tasks"}

    def post(self):
        task_data = request.get_json()
        if not task_data:
            return {'message': 'No input data provided'}, 400
        description = task_data.get('description')
        title = task_data.get('title')
        if not description and not title:
            return {'message': 'Title or description is required'}, 400
        new_task = Task(description=description, title=title)
        db.session.add(new_task)
        db.session.commit()
        return {'message': 'Task added', 'task': {'id': new_task.id,
                                                  'title': new_task.title,
                                                  'description': new_task.description,
                                                  'created_at': str(new_task.created_at),
                                                  'updated_at': str(new_task.updated_at)}}


class TaskApi(Resource):
    def get(self, task_id):
        task = db.session.query(Task).get(task_id)
        if task:
            return {'id': task.id, 'title': task.title,
                    'description': task.description,
                    'created_at': str(task.created_at),
                    'updated_at': str(task.updated_at)}
        else:
            return {'message': 'Task not found'}

    def put(self, task_id):
        task = db.session.query(Task).get(task_id)
        if task:
            task_data = request.get_json()
            title = task_data.get('title')
            description = task_data.get('description')
            if not description and not title:
                return {'message': 'Title or description is required'}, 400
            task.description = description
            task.title = title
            db.session.commit()
            return {'message': 'Task update', 'task': {'id': task.id,
                                                       'title': task.title,
                                                       'description': task.description,
                                                       'created_at': str(task.created_at),
                                                       'updated_at': str(task.updated_at)}}
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
