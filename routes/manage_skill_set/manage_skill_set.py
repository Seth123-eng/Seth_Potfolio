


from quart import (
    Blueprint, jsonify, request
)

from quart_auth import current_user

from models.skill_set_model import SkillSetTable

from helpers.db_helper import make_session
from helpers.web_security import (
    decode_with_itsdangerous
)
from helpers.authenticated_clients_manager import (
    login_required
)

from helpers.date_helper import get_current_time


manage_skill_set_bp = Blueprint('manage_skill_set_bp', __name__)


@manage_skill_set_bp.get("/delete-skill-set/<skill_set_id_>")
@login_required
async def delete_project(skill_set_id_):

    skill_set_id = decode_with_itsdangerous(skill_set_id_)
    
    if not skill_set_id:
        return jsonify({
            "success" : False,
            "message" : "Skill set not found"
        })

    async with make_session() as sess:

        skill_set_record = await sess.get(SkillSetTable, int(skill_set_id))

        if not skill_set_record:
            return jsonify({
                "success" : False,
                "message" : "skill set not found"
            })

        try:
            await sess.delete(skill_set_record)
            await sess.commit()

            return jsonify({
                "success" : True,
                "message" : "skill set Deleted"
            })

        except Exception as e:

            await sess.rollback()
            print(f"Error = {e}")

            return jsonify({
                "success" : False,
                "message" : "skill set deletion failed"
            })
    



@manage_skill_set_bp.post("/update-skill-set/<skill_set_id_>")
@login_required
async def update_project(skill_set_id_):

    form = await request.form

    skill_set_title = form.get("skill_set_title", "")
    skill_set_description = form.get("skill_set_description", "")

    skill_set_id = decode_with_itsdangerous(skill_set_id_)
    
    if not skill_set_id:
        return jsonify({
            "success" : False,
            "message" : "skill set not found"
        })

    async with make_session() as sess:

        skill_set_record = await sess.get(SkillSetTable, int(skill_set_id))

        if not skill_set_record:
            return jsonify({
                "success" : False,
                "message" : "Project not found"
            })
        
        try:
            skill_set_record.skill_set_description = skill_set_description
            skill_set_record.skill_set_title = skill_set_title

            await sess.commit()

            return jsonify({
                "success" : True,
                "message" : "skill set updated"
            })

        except Exception as e:

            await sess.rollback()
            print(f"Error = {e}")

            return jsonify({
                "success" : False,
                "message" : "skill set update failed"
            })
        


@manage_skill_set_bp.post("/register-skill-set")
@login_required
async def register_skill_set():

    form = await request.form

    skill_set_title = form.get("skill_set_title", "")
    skill_set_description = form.get("skill_set_description", "")

    user_id = int(current_user.auth_id) #type: ignore
    current_time = await get_current_time()


    async with make_session() as sess:
        
        try:
            sess.add(
                SkillSetTable(
                    skill_set_title=skill_set_title,
                    skill_set_description=skill_set_description,
                    user_id = user_id,
                    date_time = current_time
                )
            )
            
            await sess.commit()

            return jsonify({
                "success" : True,
                "message" : "skill set registered"
            })

        except Exception as e:

            await sess.rollback()
            print(f"Error = {e}")

            return jsonify({
                "success" : False,
                "message" : "Error while processing"
            })