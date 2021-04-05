"""Routes for parent Flask app."""
from flask import render_template
from flask import current_app as app


@app.route('/')
def home():
    """Landing page."""
    return render_template(
        'index.jinja2',
        title='Coomberg Terminal',
        description='Financial Data Web App',
        template='home-template',
        body="This is a homepage served with Flask."
    )