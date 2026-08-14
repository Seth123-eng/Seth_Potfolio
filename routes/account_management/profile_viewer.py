

from models.file_model import FileTable

from sqlalchemy import select

from quart import Blueprint, Response

from helpers.db_helper import make_session

from io import BytesIO


profile_viewer_bp = Blueprint("profile_viewer_bp", __name__)


@profile_viewer_bp.get("/profile/photo")
async def profile_viewer():

    async with make_session() as sess:
        profile = await sess.scalar(
            select(FileTable)
            .where(
                FileTable.is_profile.is_(True)
            )
        )

        if profile:

            return Response(
                BytesIO(profile.file_data),
                mimetype=profile.file_type
            )

        return {
            "success" : False,
            "message" : "Profile not found"
        }