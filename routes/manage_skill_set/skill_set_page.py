

from quart import (
    Blueprint, jsonify, render_template
)

from quart_auth import current_user

from models.skill_set_model import SkillSetTable

from helpers.db_helper import make_session
from helpers.web_security import (
    encode_with_itsdangerous
)
from helpers.authenticated_clients_manager import (
    get_current_user
)

from sqlalchemy import select

import os

from dotenv import load_dotenv

load_dotenv(override=True)

BASE_URL=""


skill_set_page_bp = Blueprint('skill_set_page_bp', __name__)


@skill_set_page_bp.get("/skill-set-page")
async def skill_set_page():

    current_user_ = await get_current_user()

    if current_user_:
            is_authenticated=True
    else:
        is_authenticated=False


    return await render_template("skill_set_page.html",
                                 is_authenticated=is_authenticated)



@skill_set_page_bp.get("/skill-set/fetch")
async def fetch_skill_set():

    async with make_session() as sess:

        try:
            records = await sess.scalars(
                select(SkillSetTable)
            )

            if not records:

                return jsonify({
                        "success" : True,
                        "message" : "No skill set yet"
                    })

            try:
                skill_set = [
                    {
                        "skill_set_id" : encode_with_itsdangerous(skill_set_.id),
                        "skill_set_title" : skill_set_.skill_set_title,
                        "skill_set_description" : skill_set_.skill_set_description,
                        "user_id" : encode_with_itsdangerous(skill_set_.user_id)
                    }
                    for skill_set_ in records.all()
                ]

            except Exception as e:
                print(f"Error = {e}")
                skill_set=[]
         

            return jsonify({
                "success" : True,
                "skill_set" : skill_set
            })
        except Exception as e:

            print(f"Error = {e}")

            return jsonify({
                "success" : False,
                "message" : "Failed to fetch skill set"
            })