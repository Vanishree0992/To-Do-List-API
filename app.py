from flask import Flask, request
from flask_restful import Resource, Api
from werkzeug.exceptions import BadRequest, NotFound

app = Flask(__name__)
api = Api(app)

tasks = []
task_id_counter = 1

class TaskList(Resource):
    def get(self):
        return {'tasks': tasks}, 200

    def post(self):
        global task_id_counter
        data = request.get_json()
        if not data or 'title' not in data:
            raise BadRequest('Task title is required')

        new_task = {
            'id': task_id_counter,
            'title': data['title'],
            'status': 'not completed'
        }
        tasks.append(new_task)
        task_id_counter += 1
        return new_task, 201

class Task(Resource):
    def get(self, id):
        task = next((t for t in tasks if t['id'] == id), None)
        if not task:
            raise NotFound('Task not found')
        return task, 200

    def put(self, id):
        data = request.get_json()
        task = next((t for t in tasks if t['id'] == id), None)
        if not task:
            raise NotFound('Task not found')

        # Toggle status if only status is provided
        if 'status' in data:
            if data['status'] in ['completed', 'not completed']:
                task['status'] = data['status']
            else:
                raise BadRequest("Status must be 'completed' or 'not completed'")
        # Update title if provided
        if 'title' in data:
            task['title'] = data['title']

        return task, 200

    def delete(self, id):
        global tasks
        task = next((t for t in tasks if t['id'] == id), None)
        if not task:
            raise NotFound('Task not found')

        tasks = [t for t in tasks if t['id'] != id]
        return {'message': f'Task with id {id} deleted'}, 200

api.add_resource(TaskList, '/tasks')
api.add_resource(Task, '/tasks/<int:id>')

if __name__ == '__main__':
    app.run(debug=True)
