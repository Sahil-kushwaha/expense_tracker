import sqlite3
import os
from werkzeug.security import generate_password_hash

DATABASE = 'spendly.db'

def get_db():
    """
    Returns a SQLite connection with row_factory and foreign keys enabled.
    """
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON;')
    return conn

def init_db():
    """
    Creates all tables using CREATE TABLE IF NOT EXISTS.
    """
    with get_db() as db:
        # Users table
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                created_at TEXT DEFAULT (datetime('now'))
            )
        ''')

        # Expenses table
        db.execute('''
            CREATE TABLE IF NOT EXISTS expenses (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                amount REAL NOT NULL,
                category TEXT NOT NULL,
                date TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        db.commit()

def seed_db():
    """
    Inserts sample data for development. Prevents duplicate seeding.
    """
    with get_db() as db:
        # Check if users table already has data
        user_exists = db.execute('SELECT 1 FROM users LIMIT 1').fetchone()
        if user_exists:
            return

        # Create demo user
        password_hash = generate_password_hash('demo123')
        cursor = db.execute(
            'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
            ('Demo User', 'demo@spendly.com', password_hash)
        )
        user_id = cursor.lastrowid

        # Sample expenses
        expenses = [
            (user_id, 12.50, 'Food', '2026-05-01', 'Lunch at cafe'),
            (user_id, 45.00, 'Transport', '2026-05-02', 'Weekly gas'),
            (user_id, 120.00, 'Bills', '2026-05-03', 'Electricity bill'),
            (user_id, 30.00, 'Health', '2026-05-04', 'Pharmacy'),
            (user_id, 15.00, 'Entertainment', '2026-05-05', 'Cinema ticket'),
            (user_id, 60.00, 'Shopping', '2026-05-06', 'Groceries'),
            (user_id, 10.00, 'Other', '2026-05-07', 'Parking fee'),
            (user_id, 25.00, 'Food', '2026-05-08', 'Dinner delivery'),
        ]

        db.executemany(
            'INSERT INTO expenses (user_id, amount, category, date, description) VALUES (?, ?, ?, ?, ?)',
            expenses
        )
        db.commit()
