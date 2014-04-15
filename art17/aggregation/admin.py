from flask import redirect, url_for, render_template
from art17.aggregation import aggregation


@aggregation.route('/admin/')
def admin():
    return redirect(url_for('config.form'))


@aggregation.route('/admin/checklists/')
def checklists():
    return render_template('aggregation/admin/checklists.html',
                           page='checklist')
