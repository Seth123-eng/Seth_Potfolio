

from quart import (
    Blueprint, jsonify, render_template, request
)

from models.message_model import MessageTable

from helpers.authenticated_clients_manager import (
    login_required
)
from helpers.db_helper import make_session
from helpers.date_helper import convert_to_user_time
from helpers.web_security import (
    encode_with_itsdangerous
)

from sqlalchemy import select


msgs_bp = Blueprint('msgs_bp', __name__)


@msgs_bp.get("/msgs/page")
@login_required
async def msgs_page():

    return await render_template("msgs_page.html")



@msgs_bp.post("/msgs-fetch")
@login_required
async def fetch_msgs():

    data = await request.get_json()

    time_zone=data.get("time_zone")

    print(f"time_zone = {time_zone}")

    async with make_session() as sess:

        try:
            msgs_ = await sess.scalars(
                select(MessageTable)
            )

            if not msgs_:

                return jsonify({
                        "success" : True,
                        "message" : "No messages yet"
                    })

            try:
                msgs = [
                    {
                        "msg_id" : encode_with_itsdangerous(msg.id),
                        "is_read" : msg.is_read, #True or False
                        "message_replied_to" : msg.message_replied, #True or False
                        "message_content" : msg.message_description,
                        "date_time" : convert_to_user_time(
                            date=msg.date_time,
                            zone_name=time_zone
                        ),
                        "email" : msg.email
                    }
                    for msg in msgs_.all()
                ]

            except Exception as e:
                print(f"Error = {e}")
                msgs=[]
         

            return jsonify({
                "success" : True,
                "msgs" : msgs
            })
        except Exception as e:

            print(f"Error = {e}")

            return jsonify({
                "success" : False,
                "message" : "Failed to fetch Messages"
            })