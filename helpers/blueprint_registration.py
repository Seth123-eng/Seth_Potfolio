

from app_factory import web_app


from routes.account_management.update_account_info import update_account_info_bp
from routes.account_management.profile_viewer import profile_viewer_bp

from routes.auth.login_logout_routes import login_logout_bp
from routes.auth.not_authourized_route import not_authourized_bp
from routes.auth.register_account import create_account_bp

from routes.dashboard_routes import dashboard_bp

from routes.file_handling.manage_files import manage_files_bp

from routes.manage_about_me.about_me_page import about_me_bp
from routes.manage_about_me.delete_about_me import delete_about_me_bp
from routes.manage_about_me.update_personal_description import update_personal_description_bp

from routes.manage_messages.manage_msgs import manage_msg_bp
from routes.manage_messages.msgs_page import msgs_bp
from routes.manage_messages.submit_msg import submit_msg_bp

from routes.manage_projects.manage_projects import manage_projects_bp
from routes.manage_projects.projects_page import projects_page_bp

from routes.manage_skill_set.manage_skill_set import manage_skill_set_bp
from routes.manage_skill_set.skill_set_page import skill_set_page_bp


blueprints = [
   update_account_info_bp,
   profile_viewer_bp,

   login_logout_bp,
   not_authourized_bp,
   create_account_bp,

   manage_files_bp,

   about_me_bp,
   delete_about_me_bp,
   update_personal_description_bp,

   manage_msg_bp,
   msgs_bp,
   submit_msg_bp,

   manage_projects_bp,
   projects_page_bp,

   manage_skill_set_bp,
   skill_set_page_bp,
   dashboard_bp
]

blueprints_not_registered = []

async def register_all_blueprints():
    count = 0
    
    for blueprint in blueprints:
        try:
            web_app.register_blueprint(blueprint)
            print(f"Blueprint {blueprint.name} registered 🎉")
            count += 1
        except Exception as e:
            print(f"Failed to register blueprint {blueprint.name}")
            print(f"Exception = {e}")
            
            blueprints_not_registered.append({
                "blueprint": blueprint,
                "exception": e
            })
            
    print(f"Registered Blueprints: {count} 🎉🎉")
    print(f"Blueprints not registered: {len(blueprints_not_registered)}")