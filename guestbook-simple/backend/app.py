from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector # type: ignore
import os

app = Flask(__name__)
CORS(app)

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response
# Cloud SQL configuration (use environment variables)
db_config = {
    'user': os.getenv('DB_USER', 'guestbook_user'),
    'password': os.getenv('DB_PASS', 't2`ZU9HpAUY0mGue'),
    'host': os.getenv('DB_HOST', '34.173.204.83'),
    'database': os.getenv('DB_NAME', 'guestbook_db')
}

# Initialize table (run once or on first deploy)
def init_db():
    conn = mysql.connector.connect(**db_config)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INT AUTO_INCREMENT PRIMARY KEY,
            message TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

# Run init_db only if DB_INIT is set (e.g., during setup)
if os.getenv('DB_INIT', 'false') == 'true':
    init_db()

@app.route('/messages', methods=['GET'])
def get_messages():
    conn = mysql.connector.connect(**db_config)
    c = conn.cursor()
    c.execute('SELECT * FROM messages')
    messages = [{'id': row[0], 'message': row[1]} for row in c.fetchall()]
    conn.close()
    return jsonify(messages)

@app.route('/messages', methods=['POST'])
def add_message():
    message = request.json['message']
    conn = mysql.connector.connect(**db_config)
    c = conn.cursor()
    c.execute('INSERT INTO messages (message) VALUES (%s)', (message,))
    conn.commit()
    conn.close()
    return jsonify({'message': message}), 201



if __name__ == '__main__':
    port = int(os.getenv('PORT', 80))  # Cloud Run uses PORT env var
    app.run(host='0.0.0.0', port=port)