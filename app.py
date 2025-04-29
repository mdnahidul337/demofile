from flask import Flask, render_template, request, redirect, url_for, jsonify, session
import json
import os
import uuid
from werkzeug.security import generate_password_hash, check_password_hash
from results import get_results

app = Flask(__name__)
app.secret_key = 'your_secret_key_here'

# Ensure data directory exists
os.makedirs('data', exist_ok=True)

# Initialize JSON files if they don't exist
def init_files():
    if not os.path.exists('data/users.json'):
        with open('data/users.json', 'w') as f:
            json.dump([], f)
    if not os.path.exists('data/students.json'):
        with open('data/students.json', 'w') as f:
            json.dump([], f)

init_files()

# Helper functions
def load_users():
    with open('data/users.json', 'r') as f:
        return json.load(f)

def save_users(users):
    with open('data/users.json', 'w') as f:
        json.dump(users, f, indent=4)

def load_students():
    with open('data/students.json', 'r') as f:
        return json.load(f)

def save_students(students):
    with open('data/students.json', 'w') as f:
        json.dump(students, f, indent=4)

def generate_id():
    return str(uuid.uuid4().hex)[:8]

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            data = request.get_json()
            gmail = data.get('gmail')
            username = data.get('username')
            password = data.get('password')
            name = data.get('name')
            roll = data.get('roll')
            collage = data.get('collage')
            semester = data.get('semester')
            department = data.get('department')

            users = load_users()
            students = load_students()
            
            if any(user['username'] == username for user in users):
                return jsonify({'error': 'Username already exists'}), 400
            

            user_id = generate_id()
            new_user = {
                'id': user_id,
                'gmail': gmail,
                'username': username,
                'password': generate_password_hash(password)
            }
            users.append(new_user)
            save_users(users)

            new_student = {
                'id': user_id,
                'gmail': gmail,
                'username': username,
                'name': name,
                'roll': roll,
                'department': department,
                'collage': collage,
                'semester': semester
                
            }
            students.append(new_student)
            save_students(students)

            return jsonify({'success': True, 'redirect': url_for('login')})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            data = request.get_json()
            username = data.get('username')
            password = data.get('password')

            users = load_users()
            user = next((u for u in users if u['username'] == username), None)


            if not user or not check_password_hash(user['password'], password):
                return jsonify({'error': 'Invalid username or password'}), 401

            session['user_id'] = user['id']
            session['username'] = user['username']

            return jsonify({'success': True, 'redirect': url_for('dashboard')})
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    students = load_students()
    student = next((s for s in students if s['id'] == session['user_id']), None)

    if not student:
        return redirect(url_for('login'))

    return render_template('dashboard.html', student=student)

@app.route('/update_profile', methods=['GET', 'POST'])
def update_profile():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    students = load_students()
    student = next((s for s in students if s['id'] == session['user_id']), None)

    if not student:
        return redirect(url_for('login'))

    if request.method == 'POST':
        try:
            data = request.get_json()
            if not data:
                return jsonify({'error': 'No data received'}), 400

            # Update student data
            student['name'] = data.get('name', student['name'])
            student['gmail'] = data.get('gmail', student['gmail'])
            student['roll'] = data.get('roll', student['roll'])
            student['department'] = data.get('department', student['department'])
            student['collage'] = data.get('collage', student['collage'])
            student['semester'] = data.get('semester', student['semester'])
            

            save_students(students)
            return jsonify({'success': True, 'message': 'Profile updated successfully'})
        
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    return render_template('update_profile.html', student=student)

@app.route('/reset_password', methods=['GET', 'POST'])
def reset_password():
    if request.method == 'GET':
        # Handle GET request (render the reset password form)
        return render_template('reset_password.html')
    
    # Handle POST request (process the form submission)
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data received'}), 400
        
        if 'id' in data:  # Password reset step
            required_fields = ['id', 'username', 'new_password']
            if not all(field in data for field in required_fields):
                return jsonify({'error': 'Missing required fields'}), 400
            
            if len(data['new_password']) < 8:
                return jsonify({'error': 'Password must be at least 8 characters'}), 400
                
            users = load_users()
            user = next((u for u in users if u['id'] == data['id'] and u['username'] == data['username']), None)
            
            if not user:
                return jsonify({'error': 'Invalid user credentials'}), 400
            
            user['password'] = generate_password_hash(data['new_password'])
            save_users(users)
            return jsonify({'success': True})
        
        else:  # Username verification step
            if 'username' not in data:
                return jsonify({'error': 'Username is required'}), 400
                
            users = load_users()
            user = next((u for u in users if u['username'] == data['username']), None)
            
            if not user:
                return jsonify({'error': 'Username not found'}), 404
            
            return jsonify({'user_id': user['id']})
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/get_results', methods=['POST'])
def fetch_results():
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['roll', 'year', 'exam_type']
        if not all(field in data for field in required_fields):
            return jsonify({
                'success': False,
                'error': 'Missing required fields'
            }), 400
        
        # Get results from BTEB
        results = get_results(
            roll=data['roll'],
            year=data['year'],
            exam_type=data['exam_type']
        )
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

