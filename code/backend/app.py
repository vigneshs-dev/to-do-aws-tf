import os
import logging
from flask import Flask, jsonify, request
from flask_cors import CORS
import mysql.connector
from mysql.connector import pooling
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Setup Flask app and CORS
app = Flask(__name__)
CORS(app)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Fetch database credentials from environment variables
db_host = os.getenv('DB_ENDPOINT').split(':')[0]  # Get the host without port
db_password = os.getenv('DB_PASSWORD')
db_username = 'admin'  # Replace with actual username if different

# MySQL Connection Pool Setup
db_pool = mysql.connector.pooling.MySQLConnectionPool(
    pool_name="todo_pool",
    pool_size=10,  # Define the pool size as per your app's need
    host=db_host,
    user=db_username,
    password=db_password,
    database='todo_db',
    connection_timeout=10  # Connection timeout in seconds
)

# Function to get a connection from the pool
def get_db_connection():
    try:
        conn = db_pool.get_connection()
        if conn.is_connected():
            return conn
        else:
            logger.error("Failed to get a connection from the pool.")
            raise Exception("Failed to get a connection from the pool.")
    except mysql.connector.Error as err:
        logger.error(f"Error getting connection: {err}")
        raise

# Routes for the Flask app
@app.route('/todos', methods=['GET'])
def get_todos():
    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM todos")
        todos = cursor.fetchall()
        conn.close()
        return jsonify(todos)
    except mysql.connector.Error as err:
        logger.error(f"Error fetching todos: {err}")
        return jsonify({'error': 'Failed to fetch todos'}), 500

@app.route('/todos', methods=['POST'])
def add_todo():
    try:
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
    except mysql.connector.Error as err:
        logger.error(f"Error adding todo: {err}")
        return jsonify({'error': 'Failed to add todo'}), 500

@app.route('/todos/<int:todo_id>', methods=['PUT'])
def update_todo(todo_id):
    try:
        data = request.json
        completed = data.get('completed')
        if completed is None:
            return jsonify({'error': 'Completion status is required'}), 400
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE todos SET completed = %s WHERE id = %s", (completed, todo_id))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Todo updated successfully'})
    except mysql.connector.Error as err:
        logger.error(f"Error updating todo {todo_id}: {err}")
        return jsonify({'error': 'Failed to update todo'}), 500

@app.route('/todos/<int:todo_id>', methods=['DELETE'])
def delete_todo(todo_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM todos WHERE id = %s", (todo_id,))
        conn.commit()
        conn.close()
        return jsonify({'message': 'Todo deleted successfully'})
    except mysql.connector.Error as err:
        logger.error(f"Error deleting todo {todo_id}: {err}")
        return jsonify({'error': 'Failed to delete todo'}), 500

if __name__ == '__main__':
    logger.info("Starting the Flask application...")
    app.run(host='0.0.0.0', debug=True, use_reloader=False)  # use_reloader=False to prevent Flask from creating multiple threads
