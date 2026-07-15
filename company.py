from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import db, PlacementDrive, Application
from datetime import datetime

company_bp = Blueprint('company', __name__)

def is_company():
    return current_user.is_authenticated and current_user.role == 'company' and current_user.is_approved

@company_bp.before_request
def require_company():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    if not current_user.is_authenticated or current_user.role != 'company':
        return jsonify({'error': 'Login as company.'}), 403
    if not current_user.is_approved:
        return jsonify({'error': 'Not approved yet.'}), 403

@company_bp.route('/dashboard')
def dashboard():
    drives = PlacementDrive.query.filter_by(company_id=current_user.company_profile.id).all()
    apps_count = sum([len(d.applications) for d in drives])

    drives_data = []
    for d in drives:
        drives_data.append({
            'id': d.id,
            'job_title': d.job_title,
            'deadline': d.deadline.strftime('%Y-%m-%d %H:%M'),
            'status': d.status,
            'applicants_count': len(d.applications)
        })

    return jsonify({
        'company': {
            'name': current_user.company_profile.name,
            'hr_contact': current_user.company_profile.hr_contact,
            'website': current_user.company_profile.website
        },
        'drives': drives_data,
        'apps_count': apps_count
    })

@company_bp.route('/drives/create', methods=['POST', 'OPTIONS'])
def create_drive():
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    data = request.get_json(silent=True) or {}
    title = data.get('job_title') or request.form.get('job_title')
    desc = data.get('job_description') or request.form.get('job_description')
    elig = data.get('eligibility') or request.form.get('eligibility')
    deadline_str = data.get('deadline') or request.form.get('deadline')

    if deadline_str:
        deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
    else:
        deadline = datetime.now()

    drive = PlacementDrive(
        company_id=current_user.company_profile.id,
        job_title=title,
        job_description=desc,
        eligibility=elig,
        deadline=deadline,
        status='Pending'
    )
    db.session.add(drive)
    db.session.commit()

    return jsonify({'message': 'Drive created. Pending admin approval.'})

@company_bp.route('/drives/edit/<int:drive_id>', methods=['GET', 'POST', 'OPTIONS'])
def edit_drive(drive_id):
    if request.method == 'OPTIONS':
        return jsonify({}), 200

    drive = PlacementDrive.query.get_or_404(drive_id)
    if drive.company_id != current_user.company_profile.id:
        return jsonify({'error': 'Unauthorized.'}), 403

    if request.method == 'GET':
        return jsonify({
            'id': drive.id,
            'job_title': drive.job_title,
            'job_description': drive.job_description,
            'eligibility': drive.eligibility,
            'deadline': drive.deadline.strftime('%Y-%m-%dT%H:%M'),
            'status': drive.status
        })

    # POST
    data = request.get_json(silent=True) or {}
    drive.job_title = data.get('job_title') or request.form.get('job_title')
    drive.job_description = data.get('job_description') or request.form.get('job_description')
    drive.eligibility = data.get('eligibility') or request.form.get('eligibility')
    deadline_str = data.get('deadline') or request.form.get('deadline')
    if deadline_str:
        drive.deadline = datetime.strptime(deadline_str, '%Y-%m-%dT%H:%M')
    db.session.commit()

    return jsonify({'message': 'Drive updated successfully.'})

@company_bp.route('/drives/delete/<int:drive_id>')
def delete_drive(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    if drive.company_id == current_user.company_profile.id:
        db.session.delete(drive)
        db.session.commit()
        return jsonify({'message': 'Placement drive deleted.'})
    return jsonify({'error': 'Unauthorized.'}), 403

@company_bp.route('/drives/close/<int:drive_id>')
def close_drive(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    if drive.company_id == current_user.company_profile.id:
        drive.status = 'Closed'
        db.session.commit()
        return jsonify({'message': 'Placement drive marked as closed.'})
    return jsonify({'error': 'Unauthorized.'}), 403

@company_bp.route('/applicants/<int:drive_id>')
def applicants(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    if drive.company_id != current_user.company_profile.id:
        return jsonify({'error': 'Unauthorized.'}), 403

    apps_data = []
    for a in drive.applications:
        apps_data.append({
            'id': a.id,
            'student_name': a.student.name,
            'student_contact': a.student.contact,
            'date_applied': a.date_applied.strftime('%Y-%m-%d %H:%M'),
            'resume_filename': a.student.resume_filename,
            'status': a.status
        })

    return jsonify({
        'drive_id': drive.id,
        'job_title': drive.job_title,
        'applications': apps_data
    })

@company_bp.route('/applicants/update/<int:app_id>/<status>')
def update_application(app_id, status):
    app = Application.query.get_or_404(app_id)
    if app.drive.company_id == current_user.company_profile.id:
        if status in ['Shortlisted', 'Selected', 'Rejected']:
            app.status = status
            db.session.commit()
            return jsonify({'message': f'Application status updated to {status}.', 'status': status})
    return jsonify({'error': 'Unauthorized or invalid status.'}), 403
