

from quart import (
    Blueprint, jsonify, request, render_template
)

from models.message_model import MessageTable
from models.user_model import UserTable

from helpers.authenticated_clients_manager import (
    get_current_user
)
from helpers.db_helper import make_session
from helpers.date_helper import get_current_time
from helpers.email_service.email_sending import send_email_msg
from helpers.db_helper import make_session

from sqlalchemy import select

import asyncio


submit_msg_bp = Blueprint('submit_msg_bp', __name__)


@submit_msg_bp.get('/submit-msg/page')
async def submit_msg_page():

    return await render_template("submit_msg_page.html")


@submit_msg_bp.post('/submit-msg')
async def submit_msg():
    

    form = await request.form

    message_description = form.get("message_description", "")
    email = form.get("email", "")

    if "@" not in email:
        return jsonify({
            "success" : False,
            "message" : "A valid email address is required"
        })

    async with make_session() as sess:
        admin = await sess.scalar(
            select(UserTable)
            .where(UserTable.account_type == "admin")
        )
        user_id = admin.id #type:ignore

        print(f"user_id = {user_id}")
    
        try:
            
            sess.add(
                MessageTable(
                    user_id = user_id,
                    is_read = False,
                    email = email,
                    date_time = await get_current_time(),
                    message_description = message_description,
                )
            )
            
            await sess.commit()

            asyncio.create_task(
                send_email_msg(
                    email=email,
                    max_retries=4,
                    reason="submit_contact_us_form",
                    msg=message_description
                )
            )

            return jsonify({
                "success" : True,
                "message" : "Contact Us Submitted"
            })

        except Exception as e:

            print(f"Failed submitting contact_us = {e}")
            await sess.rollback()

            return jsonify({
                "success" : False,
                "message" : "An Error occurred..."
            })