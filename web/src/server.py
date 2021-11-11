"""
Server file abstracted from the app
"""
from swinder import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=True)
    # app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)