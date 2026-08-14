

from quart import (
    Blueprint, request, url_for, jsonify, render_template
)

from quart_auth import current_user

from models.user_model import UserTable
from models.file_model import FileTable

from helpers.db_helper import make_session
from helpers.web_security import (
    password_maker, encode_with_itsdangerous
)
from helpers.date_helper import get_current_time
from helpers.authenticated_clients_manager import login_required

from sqlalchemy import select

from app_factory import web_app

import os

from dotenv import load_dotenv
load_dotenv(override=True)

FILEBASE_CDN_BASE_URL = os.getenv("FILEBASE_CDN_BASE_URL", "").strip()


update_account_info_bp = Blueprint("update_account_info_bp", __name__)


@update_account_info_bp.get("/account_management/page")
@login_required
async def update_account_page():

    return await render_template("account_management_page.html")



@update_account_info_bp.get("/user/info")
@login_required
async def get_user_info():
    
    if not await current_user.is_authenticated or current_user.auth_id is None:
        return jsonify({
            "success": False,
            "message": "User not authenticated",
            "redirect": url_for("login_logout_bp.handle_logout")
        }), 401
    
    async with make_session() as sess:
        try:
            record = await sess.scalar(
                select(UserTable)
            )
            
            if record:
                
                try:
                    response = {
                        "success": True,
                        "user_name": record.user_name,
                        "email": record.email
                    }

                    print(f"response = {response}")

                except Exception as e:
                    print(f"Exception = {e}")
                    response={}

            else:

                user_ = await sess.get(UserTable, int(current_user.auth_id))

                if user_:

                    response={
                        "success": True,
                        "user_name": user_.user_name,
                        "email": user_.email,
                        "avatar_url": None
                    }
                else:
                    response={}

            return jsonify({
                "success" : True,
                "response" : response
            })
            
        except Exception as e:
            print(f"Error fetching user info: {e}")
            return jsonify({
                "success": False,
                "message": "Failed to fetch user information"
            }), 500



@update_account_info_bp.route("/update/account_info", methods=["GET", "POST"])
@login_required
async def update_account_info():
    
    if request.method == "POST":
        
        form = await request.form
        
        current_password = form.get("current_password", "")
        new_password = form.get("new_password", "")
        user_name = form.get("user_name", "")

        
        if not current_password or not new_password:
            
            return jsonify({
                "success" : False,
                "message" : f"Please provide current password and new password."
            })
        
        async with make_session() as sess:
            
            if current_user.auth_id is not None:

                user = await sess.scalar(
                    select(UserTable)
                    .where(UserTable.id == int(current_user.auth_id))
                )
            
            if not user:
                
                return jsonify({
                    "success" : False,
                    "message" : f"User does not exist, sign up instead.."
                })
            
            
            if await web_app.bcrypt.async_check_password_hash(
                password=current_password,
                pw_hash=user.password_hash
            ):
                
                hashed_password = await password_maker(password=new_password.encode("utf-8"))

                if not hashed_password:
                    return jsonify({
                        "success" : False,
                        "message" : f"Failed to update password"
                    })
                
                try:
                    
                    user.password_hash = hashed_password
                    user.user_name = user_name
                    
                    await sess.commit()
                    
                    print("password updated successfully")
                    
                    return jsonify({
                        "success" : True,
                        "message" : f"Password updated successfully"
                    })
                    
                except Exception as e:
                    
                    print(f"Exception = {e}")
                    
                    await sess.rollback()
                    
                    return jsonify({
                        "success" : False,
                        "message" : f"Failed to update password"
                    })
            else:
                
                return jsonify({
                    "success" : False,
                    "message" : f"Invalid current password entered!!"
                })
    else:
        
        return jsonify({
            "success" : True,
            "redirect": url_for("update_account_info_bp.update_account_page")
        })
    


@update_account_info_bp.post("/update/account_info/profile_photo")
@login_required
async def update_profile_photo():

    file = (await request.files).get("file")

    if not file:

        return jsonify({
            "success": False,
            "message": "Select a file to upload"
        })


    file_name = f"{encode_with_itsdangerous(current_user.auth_id)}_{file.filename}"
    current_time = await get_current_time()
    file_data = file.read()


    async with make_session() as sess:

        profile_photo = await sess.scalar(
            select(FileTable)
            .where(
                FileTable.is_profile.is_(True)
            )
        )

        if not profile_photo:
    
            try:
                sess.add(
                    FileTable(
                        file_name = file_name,
                        file_type = file.mimetype,
                        is_profile=True,
                        file_data=file_data,
                        date_time=current_time,
                        user_id = int(current_user.auth_id) #type:ignore
                    )
                )

                await sess.commit()

                return jsonify({
                    "success" : True,
                    "message" : "Profile update in progress"
                })

            except Exception as e:

                await sess.rollback()
                print(f"Error = {e}")
                return jsonify({
                    "success" : False,
                    "message" : "Profile update failed"
                })

        else:
            try:
                profile_photo.file_name=file_name
                profile_photo.file_type=file.mimetype
                profile_photo.file_data=file_data

                await sess.commit()

                return jsonify({
                    "success" : True,
                    "message" : "Profile update in progress"
                })

            except Exception as e:

                await sess.rollback()
                print(f"Error = {e}")

                return jsonify({
                    "success" : False,
                    "message" : "Profile update failed"
                })
    


#confirm upload success
@update_account_info_bp.post("/update/account_info/confirm")
@login_required
async def confirm_upload():
    data = await request.get_json()
    profile_id = data.get('profile_id')
    success = data.get('success', False)
    
    if not success:
        return jsonify({
            "success": False,
            "message": "Upload failed"
        })
    
    # Update profile record or perform any additional logic
    return jsonify({
        "success": True,
        "message": "Upload confirmed"
    })