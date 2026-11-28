from flask import Blueprint, flash, render_template, request, session, redirect, url_for
from app.utils.auth import login_required

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
@login_required
def index():
    name = session.get('user_name')
    access_level = session.get('access_level')

    return render_template('dashboard/index.html', name=name, access_level=access_level)

@dashboard.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))  