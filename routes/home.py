"""Home routes."""
from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__)


@home_bp.route('/')
def index():
    """Home route - renders the CRUD dashboard UI."""
    return render_template("index.html")


@home_bp.route('/ui')
def ui():
    """Alias for the UI dashboard (backward compatibility)."""
    return render_template("index.html")
