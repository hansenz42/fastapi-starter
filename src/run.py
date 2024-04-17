from uvicorn import Config, Server
from app import app
from component.ConfigManager import config_manager

def main():
    config = Config(
        app=app,
        host=config_manager.get_value("server", "host"),
        port=config_manager.get_value("server", "port"),
        log_level=config_manager.get_value("log_level"),
        reload=False,
        workers=1
    )
    server = Server(config=config)

    server.run()

