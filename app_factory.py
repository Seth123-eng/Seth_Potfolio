
from config import Config

from quart import Quart, request

from quart_auth import QuartAuth
from quart_cors import cors
from quart_bcrypt import Bcrypt
from quart_rate_limiter import RateLimiter

from helpers.make_sio_server import sio_server

import asyncio
import socketio  # pip install python-socketio

import uvicorn
from dotenv import load_dotenv

load_dotenv(override=True)

def get_client_ip():
    x_forwarded_for = request.headers.get("X-Forwarded-For")
    if x_forwarded_for:
        return x_forwarded_for.split(",")[0].strip()
    return request.remote_addr


class WebApp():
    
    def __init__(self):
        
        self._quart_app=Quart(__name__)
        
        self._quart_app=cors(self._quart_app, allow_origin=["http://127.0.0.1:5000", "https://campusconnect.chat", "http://localhost:5000"])
        self._quart_app.config.from_object(Config)
        
        self._sio = sio_server
        self._sio_app = socketio.ASGIApp(
            socketio_server=self._sio, 
            other_asgi_app=self._quart_app
        )
        
        self.bcrypt = Bcrypt()
        self.bcrypt.init_app(self._quart_app)
        
        self.quart_auth_manager=QuartAuth()
        self.quart_auth_manager.init_app(self._quart_app)
        
        self.limiter=RateLimiter(key_function=get_client_ip)
        self.limiter.init_app(self._quart_app)
        
        self.register_blueprint=self._quart_app.register_blueprint
        self.route=self._quart_app.route  
        self.before_serving=self._quart_app.before_serving
        self.after_serving=self._quart_app.after_serving 
        self.after_request=self._quart_app.after_request
        self.config=self._quart_app.config
        self.errorhandler=self._quart_app.errorhandler
        self.app_context=self._quart_app.app_context              
        
    async def _run(self, host: str, port: int):
        try:
            uvconfig = uvicorn.Config(
                app=self._sio_app,
                host=host,
                port=port,
                reload=False,
                workers=4,
                log_level="info"
            )
            server = uvicorn.Server(config=uvconfig)
            await server.serve()
        except Exception as e:
            print("Shutting down")
            print(f"Exception = {e}")

    def run(self, host: str, port: int):
        asyncio.run(self._run(host, port))

web_app = WebApp()