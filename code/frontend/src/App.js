import React, { useState, useEffect } from 'react';
import axios from 'axios';

// Use the service name "backend" as the base URL in Docker
// const API_URL = 'http://backend:5000/todos';
// const API_URL = 'http://localhost:5000/todos';
const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/todos';
// const API_URL = 'http://172.17.43.144:5000/todos';

function App() {
    const [todos, setTodos] = useState([]);
    const [task, setTask] = useState('');

    useEffect(() => {
        fetchTodos();
    }, []);

    const fetchTodos = async () => {
        try {
            const response = await axios.get(API_URL);
            setTodos(response.data);
        } catch (error) {
            console.error('Error fetching todos:', error);
        }
    };

    const addTodo = async () => {
        if (!task) return;
        try {
            await axios.post(API_URL, { task });
            setTask('');
            fetchTodos();
        } catch (error) {
            console.error('Error adding todo:', error);
        }
    };

    const toggleCompletion = async (id, completed) => {
        try {
            await axios.put(`${API_URL}/${id}`, { completed: !completed });
            fetchTodos();
        } catch (error) {
            console.error('Error toggling completion:', error);
        }
    };

    const deleteTodo = async (id) => {
        try {
            await axios.delete(`${API_URL}/${id}`);
            fetchTodos();
        } catch (error) {
            console.error('Error deleting todo:', error);
        }
    };

    return (
        <div>
            <h1>Todo List</h1>
            <input
                type="text"
                value={task}
                onChange={(e) => setTask(e.target.value)}
                placeholder="Add a new task"
            />
            <button onClick={addTodo}>Add</button>
            <ul>
                {todos.map((todo) => (
                    <li key={todo.id}>
                        <span
                            style={{
                                textDecoration: todo.completed ? 'line-through' : 'none',
                                cursor: 'pointer',
                            }}
                            onClick={() => toggleCompletion(todo.id, todo.completed)}
                        >
                            {todo.task}
                        </span>
                        <button onClick={() => deleteTodo(todo.id)}>Delete</button>
                    </li>
                ))}
            </ul>
        </div>
    );
}

export default App;
