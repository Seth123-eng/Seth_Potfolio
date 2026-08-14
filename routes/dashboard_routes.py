

from quart import render_template, Blueprint, jsonify

from helpers.authenticated_clients_manager import (
    get_current_user, login_required
)
from helpers.db_helper import make_session

from sqlalchemy import select, func


from models.user_model import UserTable
from models.message_model import MessageTable


dashboard_bp = Blueprint("dashboard_bp", __name__)


@dashboard_bp.get("/")
async def dashboard():
    current_user_ = await get_current_user()
    
    # Prepare user data for template
    if current_user_:
        user_data = {
            'is_authenticated': True,
            'name': current_user_.user_name,
            'id': current_user_.id,
            'email': current_user_.email,
            'profile_picture_url': "" # TODO: Add profile picture url
        }
    else:
        user_data = {
            'is_authenticated': False,
            'name': None,
            'id': None,
            'email': None,
            'profile_picture_url': "" # TODO: Add profile picture url
        }

    async with make_session() as sess:
        admin = await sess.scalar(
            select(UserTable)
            .where(UserTable.account_type == "admin")
        )

        if not admin:

            first_name="Port"
            last_name="Folio"
        else:
            first_name = admin.user_name.split(" ")[0]
            last_name = admin.user_name.split(" ")[-1]
    
    return await render_template(
        "dashboard.html",
        current_user_=user_data,
        first_name=first_name,
        last_name=last_name
    )



@dashboard_bp.get("/new-msgs-count")
@login_required
async def get_msgs_count():

    async with make_session() as sess:

        try:

            new_msgs_count = await sess.scalar(
                select(func.count())
                .select_from(MessageTable)
                .where(
                    MessageTable.is_read.is_(False)
                )
            )

            return jsonify({
                "success" : True,
                "new_msgs_count" : new_msgs_count
            })
        
        except Exception as e:

            print(f"Error = {e}")

            return jsonify({
                "success" : True,
                "new_msgs_count" : 0
            })
            