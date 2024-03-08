from flask import Blueprint, render_template, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from flask import redirect, url_for

from app.models import User

main_bp = Blueprint('main', __name__)

# ================================================================
# ======================== NavBar ================================
# ================================================================


@main_bp.route('/index')
@main_bp.route('/')
def home():
    # Versucht, den JWT in der Anfrage zu verifizieren
    verify_jwt_in_request(optional=True)
    current_user = get_jwt_identity()
    if current_user:
        print(f'Current User: {current_user}')
        # Hier könntest du zusätzliche Logik hinzufügen, um das User-Objekt zu laden, etc.
    else:
        # Kein Benutzer identifiziert, handle den Fall entsprechend
        print('No current user')

    return render_template(
        'main/index_2.html',
        title='Home',
        # Nutze die Identität oder einen Platzhalter
        user=current_user
    )


@main_bp.route('/courses')
@jwt_required()
def courses():
    current_user = get_jwt_identity()
    return render_template(
        'main/courses.html',
        title='Courses',
        user=current_user
    )


@main_bp.route('/about')
def about():
    verify_jwt_in_request(optional=True)
    current_user = get_jwt_identity()
    return render_template(
        'main/about.html',
        title='About',
        user=current_user
    )


@main_bp.route('/contact')
@main_bp.route('/contact-us')
def contact():
    verify_jwt_in_request(optional=True)
    current_user = get_jwt_identity()
    return render_template(
        'main/contact.html',
        title='Contact',
        user=current_user
    )


# ================================================================
# ======================== Footer ================================
# ================================================================


@main_bp.route('/sitemap')
def sitemap():
    return render_template(
        'main/sitemap.html',
        title='Sitemap',
    )


@main_bp.route('/terms')
def terms():
    return render_template(
        'main/terms.html',
        title='Terms',
    )


@main_bp.route('/privacy')
def privacy():
    return render_template(
        'main/privacy.html',
        title='Privacy',
    )


@main_bp.route('/disclaimer')
def disclaimer():
    return render_template(
        'main/disclaimer.html',
        title='Disclaimer',
    )


# ================================================================
# ======================== Routes ================================
# ================================================================

@main_bp.route('/user_profile', methods=['GET', 'POST'])
@jwt_required()
def user_profile():
    email = get_jwt_identity()
    user = User.query.filter_by(email=email).first()

    if user:
        return render_template('main/user_profile.html', user=user)
    else:
        return redirect(url_for('main.home'))
