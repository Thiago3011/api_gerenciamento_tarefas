from flask import Flask, request, jsonify
from models.task import Task

app = Flask(__name__)

tasks = []
task_id_control = 1

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_control
    data = request.get_json()
    new_task = Task(id=task_id_control, title=data.get("title"), description=data.get("description", ""))
    task_id_control += 1
    tasks.append(new_task)
    print(tasks)
    
    return jsonify({"message": "Nova tarefa criada com sucesso!", "id": new_task.id})


@app.route('/tasks', methods=['GET'])
def get_tasks():
    task_list = [task.to_dict() for task in tasks]
    
    output = {
        "tasks": task_list,
        "total_tasks": len(task_list)
    }
    
    return jsonify(output)
    
@app.route('/tasks/<int:id>', methods=['GET'])
def get_task(id):
    for task in tasks:
        if task.id == id:
            return jsonify(task.to_dict())
    
    return jsonify({"message": "Não foi possível encontrar a atividade!"}), 404
    
@app.route('/tasks/<int:id>', methods=['PUT'])
def update_task(id):
    
    task = None
    
    for t in tasks:
        if t.id == id:
            task = t
    if task == None:
        return jsonify({"message": "Não foi possível encontrar a atividade!"}), 404
    
    data = request.get_json()
    task.title = data.get('title', task.title)
    task.description = data.get('description', task.description)
    task.completed = data.get('completed', task.completed)
    return jsonify({"message": "Tarefa atualizada com sucesso!"})

@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    for task in tasks:
        if task.id == id:
            tasks.remove(task)
            return jsonify({"message": "Tarefa deletada com sucesso!"})
        
    return jsonify({"message": "Não foi possível encontrar a atividade!"}), 404
    

# executando de forma manual para desenvolvimento
if __name__ == "__main__":
    app.run(debug=True) 