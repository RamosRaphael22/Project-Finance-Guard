from flask import Blueprint, render_template, request, session, redirect, url_for

dashboard = Blueprint('dashboard', __name__)

@dashboard.route('/dashboard')
def index():
    if 'user_id' not in session:
        return redirect(url_for('main.index'))

    name = session.get('user_name')
    access_level = session.get('access_level')

    return render_template('dashboard/index.html', name=name, access_level=access_level)

@dashboard.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))  