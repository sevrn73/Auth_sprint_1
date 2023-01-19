from flask import Blueprint

from api.v1.account import sign_up, login, logout, refresh, login_history, change_login, change_password

app_v1_blueprint = Blueprint('v1', __name__)

app_v1_blueprint.add_url_rule('/change_login', methods=['POST'], view_func=change_login)
app_v1_blueprint.add_url_rule('/change_password', methods=['POST'], view_func=change_password)
app_v1_blueprint.add_url_rule('/login', methods=['POST'], view_func=login)
app_v1_blueprint.add_url_rule('/login_history', methods=['GET'], view_func=login_history)
app_v1_blueprint.add_url_rule('/logout', methods=['DELETE'], view_func=logout)
app_v1_blueprint.add_url_rule('/refresh', methods=['GET'], view_func=refresh)
app_v1_blueprint.add_url_rule('/sign_up', methods=['POST'], view_func=sign_up)
