from flask import Flask, request, jsonify
from flask_mysqldb import MySQL
from datetime import datetime

app = Flask(__name__)

# Настройки подключения к MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flask_test_task'

mysql = MySQL(app)

# Маршрут для создания новой задачи
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    if not title:
        return jsonify({'error': 'Title is required'}), 400

    cur = mysql.connection.cursor()
    cur.execute("""INSERT INTO user_todos (title, description, created_at, updated_at)
                VALUES (%s, %s, %s, %s)""", (title, description, datetime.now(), datetime.now()))
    mysql.connection.commit()
    cur.close()

    task_id = cur.lastrowid
    cur = mysql.connection.cursor()
    cur.execute("""SELECT id, title, description, created_at, updated_at
                FROM user_todos WHERE id = %s""", (task_id,))
    task = cur.fetchone()
    cur.close()

    return jsonify(task), 201

# Маршрут для получения списка задач
@app.route('/tasks', methods=['GET'])
def get_tasks():
    cur = mysql.connection.cursor()
    cur.execute("""SELECT id, title, description, created_at, updated_at
                FROM user_todos""")
    tasks = cur.fetchall()
    cur.close()
    return jsonify(tasks)

# Маршрут для получения информации о задаче
@app.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    cur = mysql.connection.cursor()
    cur.execute("""SELECT id, title, description, created_at, updated_at
                FROM user_todos WHERE id = %s""", (task_id,))
    task = cur.fetchone()
    cur.close()
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task)

# Маршрут для обновления задачи
@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    cur = mysql.connection.cursor()
    cur.execute("""UPDATE user_todos
                SET title = %s, description = %s, updated_at = %s
                WHERE id = %s""", (title, description, datetime.now(), task_id))
    mysql.connection.commit()
    cur.close()

    cur = mysql.connection.cursor()
    cur.execute("""SELECT id, title, description, created_at, updated_at
                FROM user_todos WHERE id = %s""", (task_id,))
    task = cur.fetchone()
    cur.close()

    return jsonify(task), 200

# Маршрут для удаления задачи
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    cur = mysql.connection.cursor()
    cur.execute("""DELETE FROM user_todos WHERE id = %s""", (task_id,))
    mysql.connection.commit()
    cur.close()
    return jsonify({'message': 'Task deleted successfully'}), 204

if __name__ == '__main__':
    app.run(debug=True)