from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
import os

app = Flask(__name__)
CORS(app)

# Split the endpoint to get just the hostname
db_host = os.environ.get('DB_ENDPOINT', '').split(':')[0]
db_password = os.environ.get('DB_PASSWORD', '') 

db_config = {
    'host': db_host,
    'user': 'admin',
    'password': db_password,
    'database': 'todo_db'
}

# db_config = {
#     'host': 'db',
#     # 'host': 'localhost',
#     'user': 'root',
#     'password': 'melss',
#     'database': 'todo_db'
# }


def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/todos', methods=['GET'])
def get_todos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM todos")
    todos = cursor.fetchall()
    conn.close()
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def add_todo():
    data = request.json
    task = data.get('task')
    if not task:
        return jsonify({'error': 'Task is required'}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO todos (task) VALUES (%s)", (task,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Todo added successfully'}), 201

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    data = request.json
    completed = data.get('completed')
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE todos SET completed = %s WHERE id = %s", (completed, todo_id))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Todo updated successfully'})

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Todo deleted successfully'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)





