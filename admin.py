from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from models import db, User, Student, Company, PlacementDrive, Application

admin_bp = Blueprint('admin', __name__)

def is_admin():
    return current_user.is_authenticated and current_user.role == 'admin'

@admin_bp.before_request
def require_admin():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    if not is_admin():
        return jsonify({'error': 'Admin access required.'}), 403

@admin_bp.route('/dashboard')
def dashboard():
    total_students = Student.query.count()
    total_companies = Company.query.count()
    total_drives = PlacementDrive.query.count()
    total_apps = Application.query.count()
    pending_companies = User.query.filter_by(role='company', is_approved=False).count()
    pending_drives = PlacementDrive.query.filter_by(status='Pending').count()

    return jsonify({
        'total_students': total_students,
        'total_companies': total_companies,
        'total_drives': total_drives,
        'total_applications': total_apps,
        'pending_companies': pending_companies,
        'pending_drives': pending_drives
    })

@admin_bp.route('/companies')
def companies():
    search_text = request.args.get('search', '')
    if search_text:
        comps = Company.query.filter(Company.name.ilike('%' + search_text + '%')).all()
    else:
        comps = Company.query.all()

    result = []
    for c in comps:
        result.append({
            'id': c.id,
            'name': c.name,
            'hr_contact': c.hr_contact,
            'website': c.website,
            'is_approved': c.user.is_approved,
            'is_active': c.user.is_active,
            'user_id': c.user.id
        })
    return jsonify(result)

@admin_bp.route('/companies/approve/<int:user_id>')
def approve_company(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'company':
        user.is_approved = True
        db.session.commit()
    return jsonify({'message': 'Company approved.'})

@admin_bp.route('/companies/reject_or_delete/<int:user_id>')
def reject_company(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'company':
        db.session.delete(user)
        db.session.commit()
    return jsonify({'message': 'Company removed.'})

@admin_bp.route('/companies/toggle_status/<int:user_id>')
def toggle_company_status(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'company':
        user.is_active = not user.is_active
        status = 'activated' if user.is_active else 'blacklisted'
        db.session.commit()
        return jsonify({'message': f'Company {status}.', 'is_active': user.is_active})
    return jsonify({'error': 'Not a company user.'}), 400

@admin_bp.route('/students')
def students():
    search = request.args.get('search', '')
    if search:
        stds = Student.query.filter(
            (Student.name.ilike('%' + search + '%')) |
            (Student.contact.ilike('%' + search + '%'))
        ).all()
    else:
        stds = Student.query.all()

    result = []
    for s in stds:
        result.append({
            'id': s.id,
            'name': s.name,
            'contact': s.contact,
            'resume_filename': s.resume_filename,
            'is_active': s.user.is_active,
            'user_id': s.user.id
        })
    return jsonify(result)

@admin_bp.route('/students/toggle_status/<int:user_id>')
def toggle_student_status(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'student':
        user.is_active = not user.is_active
        db.session.commit()
        return jsonify({'message': 'Student status changed.', 'is_active': user.is_active})
    return jsonify({'error': 'Not a student user.'}), 400

@admin_bp.route('/students/delete/<int:user_id>')
def delete_student(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'student':
        db.session.delete(user)
        db.session.commit()
    return jsonify({'message': 'Student deleted.'})

@admin_bp.route('/drives')
def drives():
    all_drives = PlacementDrive.query.all()
    result = []
    for d in all_drives:
        result.append({
            'id': d.id,
            'company_name': d.company.name,
            'job_title': d.job_title,
            'deadline': d.deadline.strftime('%Y-%m-%d %H:%M'),
            'status': d.status
        })
    return jsonify(result)

@admin_bp.route('/drives/approve/<int:drive_id>')
def approve_drive(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    drive.status = 'Approved'
    db.session.commit()
    return jsonify({'message': 'Drive approved.'})

@admin_bp.route('/drives/reject/<int:drive_id>')
def reject_drive(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    db.session.delete(drive)
    db.session.commit()
    return jsonify({'message': 'Drive removed.'})

@admin_bp.route('/drives/applications')
def all_applications():
    apps = Application.query.all()
    result = []
    for a in apps:
        result.append({
            'id': a.id,
            'student_name': a.student.name,
            'company_name': a.drive.company.name,
            'job_title': a.drive.job_title,
            'date_applied': a.date_applied.strftime('%Y-%m-%d %H:%M'),
            'status': a.status
        })
    return jsonify(result)
