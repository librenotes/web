from project import create_app
from project.config import Config as config

if __name__ == "__main__":
    app = create_app(config)
    app.run(host="0.0.0.0")
