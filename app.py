from flask import Flask, request, render_template, send_file
from tensorflow.keras.models import load_model
from PIL import Image, ImageDraw, ImageFont
import numpy as np

app = Flask(__name__)
server = app.server

# Load your trained model
model = load_model('my_model.h5')

@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            return redirect(request.url)
        if file:
            # Process the image file
            img = Image.open(file.stream)
            img_array = np.array(img.resize((200, 200))) / 255.0
            img_array = np.expand_dims(img_array, axis=0)

            # Make a prediction
            prediction = model.predict(img_array)
            draw = ImageDraw.Draw(img)
            label = "Table" if prediction[0][0] > 0.5 else "Chair"
            draw.text((50, 50), label, (44, 44, 255),font = ImageFont.truetype("arial.ttf", size=50) )

            # Save the image to a temporary file and send it as a response
            img.save('temp.jpg')
            return send_file('temp.jpg', mimetype='image/jpeg')

    return '''
    <!doctype html>
    <title>Upload Image</title>
    <h1>Upload an image</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''

if __name__ == '__main__':
    app.run(debug=True)
