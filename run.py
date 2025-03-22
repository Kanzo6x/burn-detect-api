import os
from burn_detect_api import app

flask_app = app.create_app()

# Add a test route to verify the server is running
@flask_app.route('/')
def home():
    return 'Burn Detection API is running!'

if __name__ == "__main__":
    # Development server
    port = int(os.environ.get("PORT", 5000))
    flask_app.run(host="0.0.0.0", port=port)
else:
    # Production server (Gunicorn will use this)
    port = int(os.environ.get("PORT", 8000))
    flask_app.config['SERVER_NAME'] = f"0.0.0.0:{port}"