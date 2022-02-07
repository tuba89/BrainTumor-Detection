# Simple Flask web app to see predictions

# Import packages
from json import load
import os
import cv2
from graphviz import render
import numpy as np
from PIL import Image
import tensorflow as tf
from keras.models import load_model
from werkzeug.utils import secure_filename
from flask import Flask, request, render_template

app = Flask(__name__)

# Load our model
model = load_model("BrainTumor_Adam.h5")
print("Loading Done: Check https://127.0.0.1:5000/")


def get_className(classNo):
	if classNo==0:
		return "Healthy Brain"
	elif classNo==1:
		return "Brain Affected with a Tumor"

# Apply preproceesing before prediction
def getResult(img):
    image=cv2.imread(img)
    image = Image.fromarray(image, 'RGB')
    image = image.resize((64, 64))
    image=np.array(image)
    input_img = np.expand_dims(image, axis=0)
    # Make prediction
    result = (model.predict(input_img) > 0.5).astype("int32")
    return result


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(basepath, 
                                 'uploads',
                                 secure_filename(f.filename))
        f.save(file_path)
        value = getResult(file_path)
        result = get_className(value) 
        return result
    return None


if __name__ == '__main__':
    app.run(debug = True)
    