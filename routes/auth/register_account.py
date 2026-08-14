
from quart import (
    Blueprint, request, jsonify, render_template
)


from models.user_model import UserTable
from models.file_model import FileTable

from helpers.db_helper import make_session
from helpers.date_helper import get_current_time
from helpers.web_security import (
    password_maker,
    encode_with_itsdangerous
)

from sqlalchemy import select

import bleach


create_account_bp = Blueprint("create_account_bp", __name__)



@create_account_bp.route('/signup/page')
async def sign_up_page():
        return await render_template('auth_pages/create_account_page.html')


@create_account_bp.post("/auth/create_account")
async def create_account():

    form = await request.form
    email = bleach.clean(
        str(form.get("email"))
    )
    password = form.get("password")


    if not email or not password:
        return jsonify({
            "success": False,
            "msg": "Please provide email and password."
        })
    
    async with make_session() as sess:

        user = await sess.scalar(
            select(UserTable)
            .where(UserTable.email == email)
        )

        if user:

            return jsonify({
                "success": False,
                "msg": "Account already exists"
                })
        try:

            password_hash = await password_maker(password)
            current_time = await get_current_time()

            new_user = UserTable(
                password_hash = password_hash,
                email = email,
                user_name = email.split("@")[0],
                date_time = current_time,
                account_type="admin"
            )

            sess.add(new_user)
            await sess.commit()
           

            print("User created successfully")

            return jsonify({
                "success":  True,
                "message": "Account created successfully"
            })
        
        except Exception as e:

            print(f"Exception = {e}")

            await sess.rollback()
            return jsonify({
                "success" : False,
                "message" : f"Failed to create account."
            })