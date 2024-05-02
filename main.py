from flask import Flask, render_template
import os

app = Flask(__name__)

@app.route('/')
def index():
    # Assuming images are stored in the 'static/images' folder
    image_folder = 'static/images'
    carousel_images = sorted(os.listdir(image_folder))
    return render_template('main.html', carousel_images=carousel_images)

if __name__ == '__main__':
    app.run(debug=True)
