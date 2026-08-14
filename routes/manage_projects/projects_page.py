

from quart import (
    Blueprint, jsonify, render_template
)

from quart_auth import current_user

from models.my_projects_model import MyProjectsTable
from models.file_model import FileTable

from helpers.db_helper import make_session
from helpers.web_security import (
    encode_with_itsdangerous, decode_with_itsdangerous
)
from helpers.authenticated_clients_manager import (
    get_current_user
)

from sqlalchemy import select

import os

from dotenv import load_dotenv

load_dotenv(override=True)

FILEBASE_CDN_BASE_URL=os.getenv("FILEBASE_CDN_BASE_URL", "").strip()


projects_page_bp = Blueprint('projects_page_bp', __name__)


@projects_page_bp.get("/projects-page/<project_id>")
async def projects_page(project_id):

    current_user_ = await get_current_user()

    if current_user_:
        is_authenticated=True
    else:
        is_authenticated=False

    return await render_template("projects_page.html",
                                 is_authenticated=is_authenticated,
                                 project_id=project_id
                                 )



@projects_page_bp.get("/projects-fetch")
async def fetch_projects():

    async with make_session() as sess:

        try:
            records = await sess.execute(
                select(
                    MyProjectsTable.id,
                    MyProjectsTable.project_title
                )
            )

            if not records:

                return jsonify({
                        "success" : True,
                        "message" : "No projects yet"
                    })

            try:
                projects = [
                    {
                        "project_id" : encode_with_itsdangerous(project.id),
                        "project_title" : project.project_title
                    }
                    for project in records.all()
                ]

            except Exception as e:
                print(f"Error = {e}")
                projects=[]
         

            return jsonify({
                "success" : True,
                "projects" : projects
            })
        except Exception as e:

            print(f"Error = {e}")

            return jsonify({
                "success" : False,
                "message" : "Failed to fetch projects"
            })
        

@projects_page_bp.get("/project-details/<project_id_>")
async def project_details(project_id_):

    project_id = decode_with_itsdangerous(project_id_)

    print(f"project_id = {project_id}")
    
    if not project_id:
        return jsonify({
            "success": False,
            "message": "Project not found"
        })

    async with make_session() as sess:

        project_record = await sess.get(MyProjectsTable, int(project_id))

        
        if not project_record:
            return jsonify({
                "success": False,
                "message": "Project not found"
            })

        project_info = {
            "project_id": encode_with_itsdangerous(project_id),
            "project_title": project_record.project_title,
            "project_objectives": project_record.project_objectives,
            "project_description": project_record.project_description,
        }

        files_ = await sess.scalars(
            select(FileTable)
            .where(FileTable.project_id == int(project_id))
        )

        if files_:

            files = [
                {
                "file_id" : encode_with_itsdangerous(file.id),
                "file_url" : f"{FILEBASE_CDN_BASE_URL}/{file.file_name}"
                }
                for file in files_.all()
            ]
        else:
            files=[]

        return jsonify({
            "success": True,
            "project_details": project_info,
            "files": files
        })