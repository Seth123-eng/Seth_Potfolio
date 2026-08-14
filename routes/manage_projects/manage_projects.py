


from quart import (
    Blueprint, jsonify, request
)

from quart_auth import current_user

from models.my_projects_model import MyProjectsTable
from models.file_model import FileTable

from helpers.db_helper import make_session
from helpers.web_security import (
    decode_with_itsdangerous
)
from helpers.authenticated_clients_manager import (
    login_required
)
from helpers.date_helper import get_current_time

from sqlalchemy import select

import asyncio


manage_projects_bp = Blueprint('manage_projects_bp', __name__)


@manage_projects_bp.get("/delete-project/<project_id_>")
@login_required
async def delete_project(project_id_):

    project_id = decode_with_itsdangerous(project_id_)
    
    if not project_id:
        return jsonify({
            "success" : False,
            "message" : "Project not found"
        })

    async with make_session() as sess:

        project_record = await sess.get(MyProjectsTable, int(project_id))

        if not project_record:
            return jsonify({
                "success" : False,
                "message" : "Project not found"
            })

        project_files = await sess.scalars(
            select(FileTable)
            .where(
                FileTable.project_id == project_record.id
            )
        )
        

        try:
            if project_files:

                for file in project_files:
                    await sess.delete(file)

            await sess.delete(project_record)
            await sess.commit()

            return jsonify({
                "success" : True,
                "message" : "Project Deleted"
            })

        except Exception as e:

            await sess.rollback()
            print(f"Error = {e}")

            return jsonify({
                "success" : False,
                "message" : "Project deletion failed"
            })
    



@manage_projects_bp.post("/update-project/<project_id_>")
@login_required
async def update_project(project_id_):

    form = await request.form

    project_objectives = form.get("project_objectives", "")
    project_title = form.get("project_title", "")
    project_description = form.get("project_description", "")

    project_id = decode_with_itsdangerous(project_id_)
    
    if not project_id:
        return jsonify({
            "success" : False,
            "message" : "Project not found"
        })

    async with make_session() as sess:

        project_record = await sess.get(MyProjectsTable, int(project_id))

        if not project_record:
            return jsonify({
                "success" : False,
                "message" : "Project not found"
            })
        
        try:
            project_record.project_description = project_description
            project_record.project_title = project_title
            project_record.project_objectives = project_objectives

            await sess.commit()

            return jsonify({
                "success" : True,
                "message" : "Project updated"
            })

        except Exception as e:

            await sess.rollback()
            print(f"Error = {e}")

            return jsonify({
                "success" : False,
                "message" : "Project update failed"
            })
        


@manage_projects_bp.post("/register-project")
@login_required
async def register_project():

    form = await request.form

    project_objectives = form.get("project_objectives", "")
    project_title = form.get("project_title", "")
    project_description = form.get("project_description", "")

    user_id = int(current_user.auth_id) #type: ignore
    current_time = await get_current_time()


    async with make_session() as sess:
        
        try:
            sess.add(
                MyProjectsTable(
                    project_title=project_title,
                    project_description=project_description,
                    project_objectives=project_objectives,
                    user_id = user_id,
                    date_time = current_time
                )
            )
            
            await sess.commit()

            return jsonify({
                "success" : True,
                "message" : "Project registered"
            })

        except Exception as e:

            await sess.rollback()
            print(f"Error = {e}")

            return jsonify({
                "success" : False,
                "message" : "Error while processing"
            })