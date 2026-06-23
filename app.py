from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
import os
from datetime import datetime
from functools import wraps

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY' , 'dev-key-local') 

DATABASE = 'bank.db'

def get_db():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DATABASE):
        conn = get_db()
        cursor = conn.cursor()
        
        # Table des utilisateurs
        cursor.execute('''
            CREATE TABLE users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                full_name TEXT NOT NULL,
                account_number TEXT UNIQUE NOT NULL,
                balance REAL DEFAULT 1000,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Table des transactions
        cursor.execute('''
            CREATE TABLE transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                type TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                balance_after REAL,
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Table des virements
        cursor.execute('''
            CREATE TABLE transfers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender_id INTEGER NOT NULL,
                recipient_account TEXT NOT NULL,
                amount REAL NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'completed',
                timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (sender_id) REFERENCES users (id)
            )
        ''')
        
        conn.commit()
        conn.close()

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard'))
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        email = data.get('email')
        full_name = data.get('full_name')
        
        if not all([username, password, email, full_name]):
            return jsonify({'error': 'Tous les champs sont requis'}), 400
        
        conn = get_db()
        cursor = conn.cursor()
        
        try:
            account_number = f"FR76{username.upper()}{len(username)}{ord(username[0])}"
            cursor.execute('''
                INSERT INTO users (username, password, email, full_name, account_number)
                VALUES (?, ?, ?, ?, ?)
            ''', (username, generate_password_hash(password), email, full_name, account_number))
            
            conn.commit()
            conn.close()
            return jsonify({'success': True, 'message': 'Compte créé avec succès!'})
        except sqlite3.IntegrityError:
            conn.close()
            return jsonify({'error': 'Cet utilisateur existe déjà'}), 400
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM users WHERE username = ?', (username,))
        user = cursor.fetchone()
        conn.close()
        
        if user and check_password_hash(user['password'], password):
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['full_name'] = user['full_name']
            return jsonify({'success': True})
        else:
            return jsonify({'error': 'Identifiants invalides'}), 401
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

@app.route('/api/user/profile')
@login_required
def get_profile():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT id, username, email, full_name, account_number, balance FROM users WHERE id = ?', (session['user_id'],))
    user = cursor.fetchone()
    conn.close()
    
    return jsonify({
        'username': user['username'],
        'email': user['email'],
        'full_name': user['full_name'],
        'account_number': user['account_number'],
        'balance': user['balance']
    })

@app.route('/api/transactions')
@login_required
def get_transactions():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT * FROM transactions WHERE user_id = ? ORDER BY timestamp DESC LIMIT 20
    ''', (session['user_id'],))
    transactions = cursor.fetchall()
    conn.close()
    
    return jsonify([dict(tx) for tx in transactions])

@app.route('/api/transfer', methods=['POST'])
@login_required
def transfer():
    data = request.get_json()
    recipient_account = data.get('recipient_account')
    amount = data.get('amount')
    description = data.get('description', '')
    
    if not recipient_account or not amount or amount <= 0:
        return jsonify({'error': 'Données invalides'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Vérifier le solde
    cursor.execute('SELECT balance FROM users WHERE id = ?', (session['user_id'],))
    user = cursor.fetchone()
    
    if user['balance'] < amount:
        conn.close()
        return jsonify({'error': 'Solde insuffisant'}), 400
    
    # Vérifier que le compte destinataire existe
    cursor.execute('SELECT id FROM users WHERE account_number = ?', (recipient_account,))
    recipient = cursor.fetchone()
    
    if not recipient:
        conn.close()
        return jsonify({'error': 'Compte destinataire introuvable'}), 400
    
    try:
        # Débiter l'expéditeur
        cursor.execute('''
            UPDATE users SET balance = balance - ? WHERE id = ?
        ''', (amount, session['user_id']))
        
        # Créditer le destinataire
        cursor.execute('''
            UPDATE users SET balance = balance + ? WHERE id = ?
        ''', (amount, recipient['id']))
        
        # Enregistrer le virement
        cursor.execute('''
            INSERT INTO transfers (sender_id, recipient_account, amount, description)
            VALUES (?, ?, ?, ?)
        ''', (session['user_id'], recipient_account, amount, description))
        
        # Enregistrer les transactions
        cursor.execute('''
            INSERT INTO transactions (user_id, type, amount, description, balance_after)
            SELECT id, 'Virement sortant', ?, ?, balance FROM users WHERE id = ?
        ''', (amount, description, session['user_id']))
        
        cursor.execute('''
            INSERT INTO transactions (user_id, type, amount, description, balance_after)
            SELECT id, 'Virement entrant', ?, ?, balance FROM users WHERE id = ?
        ''', (amount, f'De {session["username"]}', recipient['id']))
        
        conn.commit()
        conn.close()
        
        return jsonify({'success': True, 'message': 'Virement effectué avec succès!'})
    except Exception as e:
        conn.close()
        return jsonify({'error': str(e)}), 500

@app.route('/api/deposit', methods=['POST'])
@login_required
def deposit():
    data = request.get_json()
    amount = data.get('amount')
    
    if not amount or amount <= 0:
        return jsonify({'error': 'Montant invalide'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute('UPDATE users SET balance = balance + ? WHERE id = ?', (amount, session['user_id']))
    cursor.execute('''
        INSERT INTO transactions (user_id, type, amount, description, balance_after)
        SELECT id, 'Dépôt', ?, 'Dépôt en espèces', balance FROM users WHERE id = ?
    ''', (amount, session['user_id']))
    
    conn.commit()
    conn.close()
    
    return jsonify({'success': True, 'message': f'Dépôt de {amount}€ effectué!'})

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
