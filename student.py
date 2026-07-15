import os
from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
from models import db, PlacementDrive, Application

student_bp = Blueprint('student', __name__)

def is_student():
    return current_user.is_authenticated and current_user.role == 'student'

@student_bp.before_request
def require_student():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    if not is_student():
        return jsonify({'error': 'Student access required.'}), 403

@student_bp.route('/dashboard')
def dashboard():
    drives = PlacementDrive.query.filter_by(status='Approved').all()

    my_apps = Application.query.filter_by(
        student_id=current_user.student_profile.id
    ).all()

    applied_ids = [a.drive_id for a in my_apps]

    available = []
    for d in drives:
        if d.id not in applied_ids:
            available.append({
                'id': d.id,
                'job_title': d.job_title,
                'company_name': d.company.name,
                'hr_contact': d.company.hr_contact,
                'eligibility': d.eligibility,
                'deadline': d.deadline.strftime('%Y-%m-%d %H:%M'),
                'job_description': d.job_description
            })

    applications_data = []
    shortlisted_count = 0
    for a in my_apps:
        if a.status in ['Shortlisted', 'Selected']:
            shortlisted_count += 1
        applications_data.append({
            'id': a.id,
            'drive_id': a.drive_id,
            'company_name': a.drive.company.name,
            'job_title': a.drive.job_title,
            'status': a.status,
            'date_applied': a.date_applied.strftime('%Y-%m-%d %H:%M')
        })

    return jsonify({
        'student': {
            'name': current_user.student_profile.name,
            'has_resume': bool(current_user.student_profile.resume_filename)
        },
        'available_drives': available,
        'applications': applications_data,
        'shortlisted_count': shortlisted_count
    })

@student_bp.route('/apply/<int:drive_id>')
def apply_drive(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)

    if drive.status != 'Approved':
        return jsonify({'error': 'Drive is not open.'}), 400

    existing = Application.query.filter_by(
        student_id=current_user.student_profile.id,
        drive_id=drive_id
    ).first()

    if existing:
        return jsonify({'error': 'Already applied.'}), 409

    new_app = Application(
        student_id=current_user.student_profile.id,
        drive_id=drive_id
    )
    db.session.add(new_app)
    db.session.commit()

    return jsonify({'message': 'Applied successfully.'})

@student_bp.route('/profile', methods=['GET', 'POST', 'OPTIONS'])
def profile():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    student = current_user.student_profile

    if request.method == 'GET':
        return jsonify({
            'name': student.name,
            'contact': student.contact,
            'resume_filename': student.resume_filename
        })

    # POST — multipart form data (file upload)
    student.name = request.form.get('name')
    student.contact = request.form.get('contact')

    if 'resume' in request.files:
        file = request.files['resume']
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
            student.resume_filename = filename

    db.session.commit()
    return jsonify({'message': 'Profile updated successfully.'})

@student_bp.route('/history')
def history():
    applications = Application.query.filter_by(
        student_id=current_user.student_profile.id
    ).all()

    result = []
    for a in applications:
        result.append({
            'id': a.id,
            'company_name': a.drive.company.name,
            'job_title': a.drive.job_title,
            'date_applied': a.date_applied.strftime('%Y-%m-%d %H:%M'),
            'deadline': a.drive.deadline.strftime('%Y-%m-%d %H:%M'),
            'status': a.status
        })
    return jsonify(result)
