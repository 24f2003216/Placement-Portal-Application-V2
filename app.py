import os
from flask import Flask, jsonify
from models import db, User
from flask_login import LoginManager

def create_app():
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'a_very_secret_key_12345'

    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///placement_portal.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 

    upload_path = os.path.join(app.root_path , "static/uploads")

    # making folder if it doesn't exist already
    os.makedirs(upload_path , exist_ok = True)

    app.config['UPLOAD_FOLDER'] = upload_path

    db.init_app(app)

    # manager login
    login_manager = LoginManager()
    # No login_view redirect — Vue handles routing
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        user_id = int(user_id)
        user_obj = User.query.get(user_id)
        return user_obj

    @login_manager.unauthorized_handler
    def unauthorized():
        return jsonify({'error': 'Unauthorized'}), 401

    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.company import company_bp
    from routes.student import student_bp

    # route register
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp , url_prefix="/admin")
    app.register_blueprint(company_bp , url_prefix="/company")
    app.register_blueprint(student_bp , url_prefix="/student")

    # CORS — allow Vite dev server (localhost:5173) with credentials
    @app.after_request
    def add_cors_headers(response):
        origin = 'http://localhost:5173'
        response.headers['Access-Control-Allow-Origin'] = origin
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, X-Requested-With'
        return response

    @app.route("/", defaults={"path": ""})
    @app.route("/<path:path>")
    def catch_all(path):
        # Only catch non-API/non-static routes
        if path.startswith(('admin', 'company', 'student', 'login', 'logout', 'register', 'api', 'static')):
            from flask import abort
            abort(404)
        return jsonify({'message': 'Flask API is running'})

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug = True, port = 5000)
