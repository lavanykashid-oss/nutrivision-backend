from app import create_app
from dotenv import load_dotenv
from flask import send_from_directory
import os



app = create_app()

# BASE_DIR = os.path.abspath(os.path.dirname(__file__))
# UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads", "meals")

# @app.route("/uploads/meals/<filename>")
# def uploaded_file(filename):

#     print("UPLOAD_FOLDER:", UPLOAD_FOLDER)
#     print("FILE:", os.path.join(UPLOAD_FOLDER, filename))
#     print("EXISTS:", os.path.exists(os.path.join(UPLOAD_FOLDER, filename)))
#     return send_from_directory(UPLOAD_FOLDER, filename)




load_dotenv()

if __name__ == "__main__":
    app.run(debug=True)