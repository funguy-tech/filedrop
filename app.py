import os
from flask import Flask, request, render_template_string
from werkzeug.utils import secure_filename

# Configure from environment variables
UPLOAD_DIR = os.environ.get('UPLOAD_DIR', '/uploads')
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Optional: set a maximum upload size (e.g., 16 MB by default)
# Uncomment the line below if you want to enforce file size limits.
# MAX_CONTENT_LENGTH = int(os.environ.get('MAX_CONTENT_LENGTH', 16 * 1024 * 1024))

DEBUG_MODE = os.environ.get('DEBUG', 'False').lower() in ['true', '1', 'yes']
FLASK_PORT = 80

app = Flask(__name__)
# If you uncomment the MAX_CONTENT_LENGTH above, set it in the app config:
# app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH

# Basic HTML page for file upload
HTML = '''
<!doctype html>
<html>
  <head><title>One Way File Drop</title></head>
  <body>
    <h1>Upload a File</h1>
    <form method="post" enctype="multipart/form-data">
      <input type="file" name="file">
      <input type="submit" value="Upload">
    </form>
  </body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files.get('file')
        if file:
            filename = secure_filename(file.filename)
            filepath = os.path.join(UPLOAD_DIR, filename)
            file.save(filepath)
            # Set file permissions: owner read/write only
            os.chmod(filepath, 0o600)
    return HTML

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=FLASK_PORT, debug=DEBUG_MODE)
