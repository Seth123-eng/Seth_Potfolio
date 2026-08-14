

from quart import (
    Blueprint, jsonify, request
)

from quart_auth import current_user

from models.personal_description_model import AboutMeTable

from helpers.db_helper import make_session
from helpers.date_helper import get_current_time
from helpers.authenticated_clients_manager import login_required
from helpers.web_security import decode_with_itsdangerous

from sqlalchemy import select


update_personal_description_bp = Blueprint('update_personal_description_bp', __name__)



@update_personal_description_bp.post("/update/personal_description")
@login_required
async def update_personal_description():

    form = await request.form

    personal_description = form.get("personal_description", "").strip()
    about_me_id_ = form.get("about_me_id_") #to be injected in form hidden field

    if personal_description == "":
        return jsonify({
            "success" : False,
            "message" : "Type something in the description area"
        })

    about_me_id = decode_with_itsdangerous(about_me_id_)


    async with make_session() as sess:

        if not about_me_id:
        
            return jsonify({
                "success" : False,
                "message" : "An error occurred... try again"
            })

        record = await sess.scalar(
            select(AboutMeTable)
            .where(
                AboutMeTable.user_id == int(current_user.auth_id)) #type:ignore
        )

        if record:
            try:

                record.personal_description = personal_description
                await sess.commit()

                return jsonify({
                    "success" : True,
                    "message" : "Personal description updated"
                })

            except Exception as e:

                await sess.rollback()
                print(f"Error = {e}")

                return jsonify({
                    "success" : False,
                    "message" : "An error occurred... try again"
                })

        return jsonify({
            "success" : False,
            "message" : "An error occurred... try again"
        })
    


@update_personal_description_bp.post("/record/personal_description")
@login_required
async def record_personal_description():

    form = await request.form
    
    personal_description = form.get("personal_description", "").strip()

    if personal_description == "":
        return jsonify({
            "success" : False,
            "message" : "Type something in the description area"
        })


    async with make_session() as sess:

        
        try:
            sess.add(
                AboutMeTable(
                    personal_description=personal_description,
                    date_time = await get_current_time(),
                    user_id = int(current_user.auth_id) #type: ignore
                )
            )

            await sess.commit()

            return jsonify({
                "success" : True,
                "message" : "Personal description updated"
            })
        except Exception as e:

            print(f"Error = {e}")
            await sess.rollback()

            return jsonify({
                "success" : False,
                "message" : "An error occurred... try again"
            })