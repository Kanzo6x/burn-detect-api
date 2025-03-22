import os
from burn_detect_api import app

flask_app = app.create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  
    flask_app.run(host="0.0.0.0", port=port)