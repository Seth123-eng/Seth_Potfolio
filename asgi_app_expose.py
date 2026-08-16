from app_factory import web_app
from helpers.blueprint_registration import register_all_blueprints
import asyncio

# Register blueprints before serving
@web_app.before_serving
async def register():
    await register_all_blueprints()

    from helpers.db_helper import Base, engine

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

# Expose the ASGI app
app = web_app._sio_app