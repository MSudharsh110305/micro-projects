import sqlite3
from datetime import date

DB = 'dietitian.db'

def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS user (
            id INTEGER PRIMARY KEY,
            age INTEGER,
            weight REAL,
            height REAL,
            gender TEXT,
            goal TEXT,
            preferences TEXT
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS intake (
            id INTEGER PRIMARY KEY,
            date TEXT,
            name TEXT,
            calories REAL,
            protein REAL,
            fat REAL,
            carbs REAL,
            sugar REAL,
            sodium REAL
        )
    ''')
    conn.commit()
    conn.close()

def save_user(profile: dict):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('DELETE FROM user')
    c.execute('''
        INSERT INTO user (age, weight, height, gender, goal, preferences)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (
        profile['age'], profile['weight'], profile['height'],
        profile['gender'], profile['goal'], profile['preferences']
    ))
    conn.commit()
    conn.close()

def load_user():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('SELECT age, weight, height, gender, goal, preferences FROM user')
    row = c.fetchone()
    conn.close()
    if row:
        return dict(zip(['age','weight','height','gender','goal','preferences'], row))
    return None

def log_intake(item: dict):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    today = date.today().isoformat()
    c.execute('''
        INSERT INTO intake (date, name, calories, protein, fat, carbs, sugar, sodium)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        today, item['name'], item['calories'], item['protein'],
        item['fat'], item['carbs'], item['sugar'], item['sodium']
    ))
    conn.commit()
    conn.close()

def get_daily_intake(date_str=None):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    if date_str is None:
        date_str = date.today().isoformat()
    c.execute('SELECT name, calories, protein, fat, carbs, sugar, sodium FROM intake WHERE date=?', (date_str,))
    rows = c.fetchall()
    conn.close()
    return rows

def delete_user():
    """Remove saved profile."""
    conn = sqlite3.connect(DB)
    conn.cursor().execute('DELETE FROM user')
    conn.commit()
    conn.close()

def delete_intake_by_date(date_str):
    """Remove all intake entries for a given date."""
    conn = sqlite3.connect(DB)
    conn.cursor().execute('DELETE FROM intake WHERE date = ?', (date_str,))
    conn.commit()
    conn.close()

def delete_all_intake():
    """Remove every intake record."""
    conn = sqlite3.connect(DB)
    conn.cursor().execute('DELETE FROM intake')
    conn.commit()
    conn.close()

def get_intake_between(start_date, end_date):
    """Return list of (date, total_calories) between two dates inclusive."""
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute('''
        SELECT date, SUM(calories) 
        FROM intake 
        WHERE date BETWEEN ? AND ?
        GROUP BY date
        ORDER BY date
    ''', (start_date, end_date))
    rows = c.fetchall()
    conn.close()
    return rows