'''
	Main app for vislang.ai
'''
import random, io, time
import requests as http_requests

from flask import Flask, request, redirect, flash, url_for
from flask import render_template
from flask_talisman import Talisman
import validators

from whoosh import index
from whoosh.qparser import QueryParser

from werkzeug.utils import secure_filename
from werkzeug.exceptions import RequestEntityTooLarge

import transformers
import meme_demo
from utils import resize_image, center_crop_image, image2string, rotate_image_if_needed

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

@app.route('/', methods=["GET"])
def main():
	return render_template('index.html')

@app.route('/simple-demo', methods = ["GET", "POST"])
def simple_demo():
	if request.method == "GET":
		return render_template('index.html')

	text_input = request.form.get('text_input')
	text_input = str(text_input)
	print("get text input: "+text_input)

	start_time = time.time()
	imgs = meme_demo.generate_meme(text_input)
	debug_str = 'process took %.2f seconds' % (time.time() - start_time)

	output_image_str = []
	for img in imgs:
		img = img.convert('RGB')
		img = resize_image(img, 224)

		output_image_str.append(image2string(img))

	return {'filename': text_input, 
			'input_image': output_image_str[0], 
			'output_image': output_image_str[1],
			'debug_str': debug_str}

if __name__ == '__main__':
    # Used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='localhost', port=8080, debug=True)
