from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from .models import db, User

routes_bp = Blueprint('routes', __name__)

@routes_bp.route('/dashboard', methods=['GET'])
@jwt_required()
def dashboard():
    user = get_jwt_identity()
    role = user['role']

    if role == 'Superadmin':
        users = User.query.all()
    elif role == 'Admin':
        users = User.query.filter_by(creator=user['username']).all()
    else:
        return jsonify({'msg': 'Access denied'}), 403

    return jsonify({'users': [user.username for user in users]}), 200

