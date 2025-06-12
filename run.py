import os
from burn_detect_api import app

flask_app = app.create_app()

@flask_app.errorhandler(500)
def handle_500(e):
    return {'error': 'Internal Server Error'}, 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5001))
    flask_app.run(host="0.0.0.0", port=port)