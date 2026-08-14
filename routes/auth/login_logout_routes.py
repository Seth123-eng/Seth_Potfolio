
from quart import (
    Blueprint, request, url_for, redirect,
    session, jsonify
)

from quart_auth import AuthUser, login_user, logout_user

from helpers.db_helper import make_session
from helpers.authenticated_clients_manager import login_required


from models.user_model import UserTable

from sqlalchemy import select

from app_factory import web_app

#from werkzeug.security import check_password_hash


import bleach


login_logout_bp = Blueprint("login_logout_bp", __name__)


@login_logout_bp.post("/auth/login")
async def handle_login():
    
    form = await request.form
    
    email = bleach.clean(
        str(form.get("email", "")).strip()
    )
    password = form.get("password", "")
    
    async with make_session() as sess:
        
        user = await sess.scalar(
            select(UserTable)
            .where(UserTable.email == email)
        )
        
        if not user:
            
            return jsonify({
                "success" : False,
                "message" : f"User does not exist, sign up instead.."
            })
        
        
        if await web_app.bcrypt.async_check_password_hash(
            password=password,
            pw_hash=user.password_hash
        ):
            
            
            login_user(AuthUser(str(user.id)))
            
            return jsonify({
                "success": True,
                "redirect" : url_for("dashboard_bp.dashboard")
            })
            
            
        return jsonify({
            "success" : False,
            "message" : f"Invalid login credentials entered!!"
        })
        
        
        
@login_logout_bp.route("/logout")
@login_required
async def handle_logout():
    
    session.clear()
    logout_user()
    
    return redirect(url_for('create_account_bp.sign_up_page'))