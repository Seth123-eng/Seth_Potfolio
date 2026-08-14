

from quart import (
    Blueprint, jsonify
)

from quart_auth import current_user

from models.personal_description_model import AboutMeTable

from helpers.db_helper import make_session
from helpers.authenticated_clients_manager import login_required
from helpers.web_security import decode_with_itsdangerous

from sqlalchemy import select


delete_about_me_bp = Blueprint('delete_about_me_bp', __name__)



@delete_about_me_bp.get("/delete/about_me/<about_me_id_>")
@login_required
async def delete_personal_description(about_me_id_):

    about_me_id = decode_with_itsdangerous(about_me_id_)

    if not about_me_id:
        return jsonify({
            "success" : False,
            "message" : "An error occurred... try again"
        })

    async with make_session() as sess:

        record = await sess.scalar(
            select(AboutMeTable)
            .where(
                AboutMeTable.user_id == int(current_user.auth_id)) #type:ignore
        )

        if record:
            try:

                await sess.delete(record)
                await sess.commit()

                return jsonify({
                    "success" : True,
                    "message" : "Personal description deleted"
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