

from quart import (
    Blueprint, jsonify, render_template
)

from quart_auth import current_user

from models.personal_description_model import AboutMeTable
from models.file_model import FileTable

from helpers.db_helper import make_session
from helpers.web_security import encode_with_itsdangerous
from helpers.authenticated_clients_manager import (
    get_current_user
)

from sqlalchemy import select

import os

from dotenv import load_dotenv
load_dotenv(override=True)


about_me_bp = Blueprint('about_me_bp', __name__)


FILEBASE_CDN_BASE_URL=os.getenv("FILEBASE_CDN_BASE_URL", "").strip()


@about_me_bp.get("/about_me/page")
async def about_me_page():

    current_user_ = await get_current_user()

    if current_user_:
        is_authenticated=True
    else:
        is_authenticated=False

    return await render_template("about_me_page.html",
                                 is_authenticated=is_authenticated)



@about_me_bp.post("/get/about_me")
async def fetch_about_me():

    async with make_session() as sess:

        
        try:
            about_me_record = await sess.scalar(
                select(AboutMeTable)
            )

            profile_pic = await sess.scalar(
                select(FileTable)
                .where(
                    FileTable.is_profile.is_(True)
                )
            )

            if not profile_pic:
                profile_pic=None

                profile_link = ""
            else:
                profile_link = f"{FILEBASE_CDN_BASE_URL}/{profile_pic.file_name}"


            if not about_me_record:

                return jsonify({
                        "success" : False,
                        "message" : "Failed to fetch personal description"
                    })

            signed_about_me_id=encode_with_itsdangerous(about_me_record.id)

            data = {
                "about_me_description_id" : signed_about_me_id,
                "about_me_description" : about_me_record.personal_description,
                "profile_pic" : f"{profile_link}"
            }


            return jsonify({
                "success" : True,
                "about_me_description" : data
            })
        except Exception as e:

            print(f"Error = {e}")

            return jsonify({
                "success" : False,
                "message" : "Failed to fetch personal description"
            })