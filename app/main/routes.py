from flask import Blueprint

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def home():
    return "This is the home page."


@main_bp.route('/about')
def about():
    return "Hier könnte ihre Werbung stehen!"
