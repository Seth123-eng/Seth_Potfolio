

from quart import (
    Blueprint, jsonify, request, Response
)

from quart_auth import current_user

from models.file_model import FileTable

from helpers.authenticated_clients_manager import (
    login_required
)
from helpers.db_helper import make_session
from helpers.date_helper import get_current_time
from helpers.web_security import (
    decode_with_itsdangerous
)

from sqlalchemy import select

from io import BytesIO

import asyncio


manage_files_bp = Blueprint('manage_files_bp', __name__)


@manage_files_bp.post("/project/upload-file/<project_id_>")
@login_required
async def handle_file_upload(project_id_):

    project_id = decode_with_itsdangerous(project_id_)

    if not project_id:
        return jsonify({
            "success" : False,
            "message" : "Project not Found",
        })

    file = (await request.files).get("file")

    if not file:

        return jsonify({
            "success" : False,
            "message" : "Select a file to upload"
        })

    file_name = f"{current_user.auth_id}_{file.filename}"
    file_type = file.mimetype

    file_data = file.read()


    async with make_session() as sess:

        try:

            sess.add(
                FileTable(
                    file_name = file_name,
                    file_type=file_type,
                    is_profile=False,
                    project_id=project_id,
                    file_data=file_data,
                    date_time = await get_current_time(),
                    user_id=int(current_user.auth_id) #type:ignore
                )
            )

            await sess.commit()

            return jsonify({
                "success" : True,
                "message" : "File upload in progress"
            })

        except Exception as e:

            print(f"Error = {e}")
            await sess.rollback()

            return jsonify({
                "success" : False,
                "message" : "File upload Failed"
            })
        


@manage_files_bp.get("/project/delete-file/<file_id_>")
@login_required
async def handle_file_delete(file_id_):

    file_id = decode_with_itsdangerous(file_id_)
    
    if not file_id:
        return jsonify({
            "success" : False,
            "message" : "File not found"
        })

    async with make_session() as sess:

        file_record = await sess.get(FileTable, int(file_id))
        

        if file_record:
            try:
                await sess.delete(file_record)
                await sess.commit()

                return jsonify({
                    "success" : True,
                    "message" : "File deleted"
                })

            except Exception as e:

                await sess.rollback()
                print(f"Error = {e}")

                return jsonify({
                    "success" : False,
                    "message" : "File deletion failed"
                })

        return jsonify({
            "success" : False,
            "message" : "An error occurred... try again"
        })



@manage_files_bp.get("/view_file/<file_id_>")
async def profile_viewer(file_id_):

    file_id = decode_with_itsdangerous(file_id_)

    if not file_id:
        return {
            "success" : False,
            "message" : "File not found"
        }

    async with make_session() as sess:
        profile = await sess.scalar(
            select(FileTable)
            .where(
                FileTable.id == int(file_id)
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