from project import create_app
from project.config import Config as config

app = create_app(config)

if __name__ == "__main__":
    app.run(host="0.0.0.0")
