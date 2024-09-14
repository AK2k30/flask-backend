from flask import Blueprint, request, jsonify
from .models import Task
from . import db

main = Blueprint('main', __name__)

@main.route('/')
def ping_server():
    return 'Server is up and running'

@main.route('/tasks', methods=['POST'])
def create_task():
    data = request.json
    new_task = Task(name=data['name'])
    db.session.add(new_task)
    db.session.commit()
    return jsonify(new_task.to_dict()), 201

@main.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.filter_by(is_deleted=False).all()
    return jsonify([task.to_dict() for task in tasks])

@main.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.json
    task.name = data.get('name', task.name)
    task.updated_at = db.func.now()
    db.session.commit()
    return jsonify(task.to_dict())

@main.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    task.is_deleted = True
    task.updated_at = db.func.now()
    db.session.commit()
    return '', 204

@main.route('/tasks', methods=['DELETE'])
def delete_all_tasks():
    Task.query.update({Task.is_deleted: True, Task.updated_at: db.func.now()})
    db.session.commit()
    return '', 204