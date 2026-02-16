"""DataScope Enhanced - User Routes"""
from flask import Blueprint, request, jsonify
from src.models.user import db, User

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([u.to_dict() for u in users])

@user_bp.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    user = User(
        username=data.get('username'),
        email=data.get('email'),
        role=data.get('role', 'viewer'),
    )
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

@user_bp.route('/status', methods=['GET'])
def status():
    return jsonify({
        'status': 'online',
        'service': 'DataScope Enhanced',
        'version': '1.0.0',
    })
