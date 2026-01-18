from flask import Blueprint, render_template

projeto_bp = Blueprint('projeto', __name__)

@projeto_bp.route('/projeto')
def projeto():
    return render_template('projeto.html')
  