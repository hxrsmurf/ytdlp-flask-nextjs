from flask import Blueprint, Flask, jsonify, request, redirect
from classes import Testing

blueprint_testing_bp = Blueprint('blueprint_testing', __name__, url_prefix='/blueprint_testing')

@blueprint_testing_bp.route('/')
def blueprint_testing_page():
    query_testing = Testing.Testing.query().all()
    print(query_testing)
    return('Hello World')