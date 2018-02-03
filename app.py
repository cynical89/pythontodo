import os.path
from flask import Flask, jsonify, abort, make_response, request, send_from_directory, url_for

app = Flask(__name__, static_url_path="/static")

tasks = [
    {
        "id": 1,
        "title": "Buy groceries",
        "description": "Milk, Cheese, Potatoes",
        "done": False
    }
]

@app.route("/")
def root():
    return app.send_static_file("index.html")

@app.route("/js/<path:path>")
def send_js(path):
    return send_from_directory("js", path)

# Get all tasks.
@app.route("/tasks", methods=["GET"])
def get_tasks():
    new_task_list = filter_if_done(tasks)
    return jsonify({"tasks": [make_public_task(task) for task in new_task_list]})

# Get a single task
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    task = [task for task in tasks if task["id"] == task_id]
    if len(task) == 0:
        abort(404)
    return jsonify({"task": task[0]})

#Create a new task
@app.route("/tasks", methods=["POST"])
def create_task():
    if not request.json or not "title" in request.json:
        abort(400)
    task = {
        "id": tasks[-1]["id"] + 1,
        "title": request.json["title"],
        "description": request.json.get("description", ""),
        "done": False
    }
    tasks.append(task)
    return jsonify({"task": task}), 201

# Update tasks
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    task = [task for task in tasks if task["id"] == task_id]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if "title" in request.json and type(request.json["title"]) is not unicode:
        abort(400)
    if "description" in request.json and type(request.json["description"]) is not unicode:
        abort(400)
    if "done" in request.json and type(request.json["done"]) is not bool:
        abort(400)
    task[0]["title"] = request.json.get("title", task[0]["title"])
    task[0]["description"] = request.json.get("description", task[0]["description"])
    task[0]["done"] = request.json.get("done", task[0]["done"])
    return jsonify({"task": task[0]})

#Remove tasks
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    task = [task for task in tasks if task["id"] == task_id]
    if len(task) == 0:
        abort(404)
    tasks.remove(task[0])
    return jsonify({"result": True})

# Helpers
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not found : {}".format(error)}), 404)

def make_public_task(task):
    task["uri"] = url_for("get_task", task_id=task["id"], _external=True)
    return task

def filter_if_done(task_list):
    for task in task_list:
        if task["done"] == False:
            yield task
            

if __name__ == "__main__":
    app.run(debug=True)