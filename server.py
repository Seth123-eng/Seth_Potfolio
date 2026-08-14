
#import hypercorn.asyncio
#from hypercorn.config import Config
    
from app_factory import web_app

from quart import redirect, url_for

from quart_auth import Unauthorized

from helpers.db_helper import Base, engine
from helpers.blueprint_registration import register_all_blueprints

import os

from dotenv import load_dotenv
load_dotenv(override=True)

Host=os.getenv("Host", "").strip()

    
@web_app.before_serving
async def startup():

    await register_all_blueprints()
    
    async with web_app.app_context():
        
        async with engine.begin() as conn:
            
            try:
                
                await conn.run_sync(Base.metadata.create_all)
                #await conn.run_sync(Base.metadata.reflect(bind=engine))
                #await conn.run_sync(Base.metadata.drop_all)
                print("Database Tables Created")
                
            except Exception as e:
                print(f"EXCEPTION = {e}")


@web_app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-store, no-cache, must-revalidate, max-age=0"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response


@web_app.errorhandler(Unauthorized)
async def handle_unauthorized_users(e):
    print(f"Exception = {e}")    
    return redirect(url_for('not_authourized_bp.not_authourized_page'))


if __name__ == '__main__':

    #config = Config()
    #config.bind = ["0.0.0.0:5000"]
    #config.debug = True 
    #config.use_reloader = True

    #asyncio.run(hypercorn.asyncio.serve(app, config))
    
    web_app.run(Host, 5000)