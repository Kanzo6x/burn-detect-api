import os
from burn_detect_api.app import create_app

flask_app = create_app()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # Railway provides a port
    flask_app.run(host="0.0.0.0", port=port)