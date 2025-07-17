from flask import Flask, render_template, request
from rembg import remove
import os
from PIL import Image
from io import BytesIO

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    filename = None
    if request.method == 'POST':
        file = request.files['image']
        if file:
            input_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            output_path = os.path.join(app.config['UPLOAD_FOLDER'], 'no-bg-' + file.filename)
            file.save(input_path)
            with open(input_path, 'rb') as i:
                input_img = i.read()
                output_img = remove(input_img)
                img = Image.open(BytesIO(output_img)).convert("RGBA")
                img.save(output_path)
            filename = 'no-bg-' + file.filename
    return render_template('index.html', filename=filename)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
