

from quart import (
    Blueprint, jsonify, request
)

from models.message_model import MessageTable

from helpers.authenticated_clients_manager import (
    login_required
)
from helpers.db_helper import make_session
from helpers.email_service.email_sending import send_email_msg
from helpers.web_security import (
    decode_with_itsdangerous
)


manage_msg_bp = Blueprint('manage_msg_bp', __name__)


@manage_msg_bp.get('/msg/delete/<msg_id_>')
@login_required
async def delete_msg(msg_id_):

    msg_id = decode_with_itsdangerous(msg_id_)

    if not msg_id:

        return jsonify({
            "success" : False,
            "message" : "An Error occurred..."
        })

    async with make_session() as sess:
        
        try:
            
            msg_record = await sess.get(MessageTable, int(msg_id))

            if msg_record:
                await sess.delete(msg_record)
                await sess.commit()

                return jsonify({
                    "success" : True,
                    "message" : "Message send, I will get back to you via your email"
                })
            return jsonify({
                "success" : False,
                "message" : "An Error occurred... message not send"
            })

        except Exception as e:

            await sess.rollback()

            print(f"Failed submitting contact_us = {e}")
            return jsonify({
                "success" : False,
                "message" : "An Error occurred... message not send"
            })
        



@manage_msg_bp.get('/msg/mark-as-read/<msg_id_>')
@login_required
async def msg_mark_as_read(msg_id_):

    msg_id = decode_with_itsdangerous(msg_id_)

    if not msg_id:

        return jsonify({
            "success" : False,
            "message" : "An Error occurred..."
        })

    async with make_session() as sess:
        
        try:
            
            msg_record = await sess.get(MessageTable, int(msg_id))

            if msg_record:
                msg_record.is_read = True
                await sess.commit()

                return jsonify({
                    "success" : True,
                    "message" : "marked message as read"
                })

        except Exception as e:

            await sess.rollback()

            print(f"Error = {e}")
            return jsonify({
                "success" : False,
                "message" : "Failed to mark message as read"
            })
        


@manage_msg_bp.post('/msg/reply-to-email/<msg_id_>')
@login_required
async def msg_reply_to_email(msg_id_):

    msg_id = decode_with_itsdangerous(msg_id_)

    form = await request.form
    reply_content = form.get("reply_content", "")
    
    if not msg_id:

        return jsonify({
            "success" : False,
            "message" : "An Error occurred..."
        })

    async with make_session() as sess:
            
        try:
            
            msg_record = await sess.get(MessageTable, int(msg_id))

            if msg_record:
                msg_record.message_replied = True
                msg_record.is_read = True
                await sess.commit()

                await send_email_msg(
                    email=msg_record.email,
                    reason="send_reply_email",
                    msg=reply_content
                )

                return jsonify({
                    "success" : True,
                    "message" : "replied to client message"
                })

        except Exception as e:
        
            await sess.rollback()

            print(f"Error = {e}")
            return jsonify({
                "success" : False,
                "message" : "message reply failed"
            })