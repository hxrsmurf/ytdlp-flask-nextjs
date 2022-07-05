from flask import Blueprint, Flask, jsonify, request, redirect

blueprint_testing_bp = Blueprint('blueprint_testing', __name__, url_prefix='/blueprint_testing')

@blueprint_testing_bp.route('/')
def blueprint_testing_page():
    return('Hello World')