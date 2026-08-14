from models.user_model import UserTable
from quart_auth import current_user
from functools import wraps
from quart import render_template, redirect, url_for
from helpers.db_helper import make_session
from sqlalchemy import select
import typing as t


async def get_current_user() -> t.Optional[UserTable]:
    """
    Get the currently authenticated user.
    Returns None if not authenticated or any error occurs.
    """
    if current_user.auth_id is None:
        return None
        
    async with make_session() as sess:
        try:
            user = await sess.scalar(
                select(UserTable)
                .where(UserTable.id == int(current_user.auth_id))
            )
            
            if not user:
                print("No user found for auth_id:", current_user.auth_id)
                return None
            
            print("Grabbed the current user 🎉🎉")
            return user
            
        except Exception as e:
            print("Unable to grab the currently logged in client")
            print(f"Exception = {e}")
            return None



def login_required(func) -> t.Any:
    
    @wraps(func)
        
    async def decorated_func(*args, **kwargs):

        async with make_session() as sess:

            if current_user.auth_id is not None:
            
                try:
                    user = await sess.scalar(
                        select(UserTable)
                        .where(
                            UserTable.id == int(current_user.auth_id)
                        )
                    )

                    if not user:
                        return redirect(url_for('not_authourized_bp.not_authourized_page'))
            
                    print("User with the role found. 🎉🎉")

                except Exception as e:

                    print(f"Exception = {e}")

                    return await render_template("not_authorised.html")
            else:
                return redirect(url_for('not_authourized_bp.not_authourized_page'))
        
        return await func(*args, **kwargs)
    
    return decorated_func