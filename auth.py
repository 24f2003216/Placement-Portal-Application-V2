from flask import Blueprint, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Student, Company

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/api/me')
def me():
    if current_user.is_authenticated:
        return jsonify({
            'username': current_user.username,
            'role': current_user.role
        })
    return jsonify({'error': 'Not authenticated'}), 401

@auth_bp.route('/login', methods=['GET', 'POST', 'OPTIONS'])
def login():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    if request.method == 'GET':
        if current_user.is_authenticated:
            return jsonify({'role': current_user.role, 'username': current_user.username})
        return jsonify({'error': 'Not logged in'}), 401

    # POST
    data = request.get_json(silent=True) or {}
    username = data.get('username') or request.form.get('username')
    password = data.get('password') or request.form.get('password')

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({'error': 'User not found.'}), 401

    if not check_password_hash(user.password, password):
        return jsonify({'error': 'Wrong password.'}), 401

    if not user.is_active:
        return jsonify({'error': 'Account is blocked.'}), 403

    if user.role == 'company' and not user.is_approved:
        return jsonify({'error': 'Waiting for approval.'}), 403

    login_user(user)
    return jsonify({'message': 'Logged in.', 'role': user.role, 'username': user.username})

@auth_bp.route('/register/student', methods=['POST', 'OPTIONS'])
def register_student():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    data = request.get_json(silent=True) or {}
    username = data.get('username') or request.form.get('username')
    password = data.get('password') or request.form.get('password')
    name = data.get('name') or request.form.get('name')
    contact = data.get('contact') or request.form.get('contact')

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists.'}), 409

    hashed = generate_password_hash(password)
    user = User(username=username, password=hashed, role='student', is_approved=True)
    db.session.add(user)
    db.session.flush()

    student = Student(user_id=user.id, name=name, contact=contact)
    db.session.add(student)
    db.session.commit()

    return jsonify({'message': 'Student registered successfully.'})

@auth_bp.route('/register/company', methods=['POST', 'OPTIONS'])
def register_company():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    data = request.get_json(silent=True) or {}
    username = data.get('username') or request.form.get('username')
    password = data.get('password') or request.form.get('password')
    name = data.get('name') or request.form.get('name')
    hr = data.get('hr_contact') or request.form.get('hr_contact')
    website = data.get('website') or request.form.get('website')

    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username already exists.'}), 409

    hashed = generate_password_hash(password)
    user = User(username=username, password=hashed, role='company', is_approved=False)
    db.session.add(user)
    db.session.flush()

    comp = Company(user_id=user.id, name=name, hr_contact=hr, website=website)
    db.session.add(comp)
    db.session.commit()

    return jsonify({'message': 'Company registered. Waiting for admin approval.'})

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logged out.'})
