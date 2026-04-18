import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), 'dpres.db')

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS scores (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            score INTEGER,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        )
    ''')
    conn.commit()
    conn.close()

def create_user(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

def validate_login(username, password):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT id FROM users WHERE username = ? AND password = ?', (username, password))
    user = c.fetchone()
    conn.close()
    if user:
        return user[0]
    return None

def save_score(user_id, score):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('INSERT INTO scores (user_id, score) VALUES (?, ?)', (user_id, score))
    conn.commit()
    conn.close()

def get_dashboard_stats():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    
    # Total users
    c.execute('SELECT COUNT(*) FROM users')
    total_users = c.fetchone()[0] or 0
    
    # Average score
    c.execute('SELECT AVG(score) FROM scores')
    avg_score = c.fetchone()[0] or 0
    
    # Total simulations (using score entries as a proxy for quiz runs)
    c.execute('SELECT COUNT(*) FROM scores')
    total_sims = c.fetchone()[0] or 0
    
    # Recent scores
    c.execute('''
        SELECT u.username, s.score, s.timestamp 
        FROM scores s 
        JOIN users u ON s.user_id = u.id 
        ORDER BY s.timestamp DESC LIMIT 50
    ''')
    recent_scores = c.fetchall()
    
    conn.close()
    return total_users, avg_score, total_sims, recent_scores

# Initialize DB on import
init_db()
