from flask import Blueprint, render_template, request, session, redirect, url_for

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
def index():
    if 'user_id' not in session:
        return redirect(url_for('main.index'))
    return render_template('dashboard/index.html')