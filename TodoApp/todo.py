from flask import Flask, request, make_response, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

PORT = 8000
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todoApp.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
app.app_context().push()


# create the structure of the database table
class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(200), nullable=False)


# API to create a task
@app.route('/addNewTask', methods=["POST"])
def addTask():
    requestBody = request.json
    try:
        #create a Todo object and commit to add the task in database
        todo = Todo(title=requestBody["task_title"],
                    status=requestBody["status"])
        db.session.add(todo)
        db.session.commit()
        return make_response(jsonify({"Success": "Task Addedd"}), 200)
    except:
        return make_response(jsonify({"Error": "Something went wrong"}), 500)


# API to get all tasks
@app.route('/getTasks', methods=["GET"])
def getTasks():
    #queries all the rows in the database and returns a list of Todo objects
    todo = Todo.query.all()
    if (todo):
        dict = {}
        for i in todo:
            d1 = {"Title": i.title, "date": str(i.date), "status": i.status}
            dict[i.sno] = d1

        return jsonify(dict)
    else:
        return make_response(jsonify({"Empty": "You don't have any tasks"}), 500)


# API to update a task
@app.route('/updateTask', methods=["PUT"])
def updateTask():
    requestBody = request.json
    #filters the database for a given sno and returns a matched row
    updatedTodo = Todo.query.filter_by(sno=requestBody["sno"]).first()
    if (updatedTodo):
        updatedTodo.title = requestBody["task_title"]
        updatedTodo.date = datetime.now()
        db.session.add(updatedTodo)
        db.session.commit()
        return make_response(jsonify({"success": "Task Updated"}), 200)
    else:
        return make_response(jsonify({"Error": "Task not found"}), 500)


# API to delete tasks
@app.route('/deleteTask/<sno>', methods=["DELETE"])
def deleteTask(sno):
    getTodo = Todo.query.filter_by(sno=sno).first()
    if (getTodo):
        db.session.delete(getTodo)
        db.session.commit()
        return make_response(jsonify({"success": "Task Deleted"}), 200)
    else:
        return make_response(jsonify({"Error": "Task not found"}), 500)


# API to change status of tasks
@app.route('/changeTaskStatus/<sno>', methods=["PUT"])
def changeTaskStatus(sno):
    getTodo = Todo.query.filter_by(sno=sno).first()
    if (getTodo):
        if (getTodo.status == "incomplete"):
            getTodo.status = "completed"
        else:
            getTodo.status = "incomplete"
        db.session.add(getTodo)
        db.session.commit()
        return make_response(jsonify({"success": "Status changed"}), 200)
    else:
        return make_response(jsonify({"Error": "Task not found"}), 500)


if __name__ == "__main__":
    app.run(debug=True, port=PORT)
