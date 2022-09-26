import os
import urllib.request
from app import app
from flask import Flask, request, redirect, jsonify
from werkzeug.utils import secure_filename
import tfidfnlpcode as tf
from os import path

ALLOWED_EXTENSIONS = set(['csv'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/file-upload', methods=['POST'])
def upload_file():
	# check if the post request has the file part
	if 'file' not in request.files:
		resp = jsonify({'message' : 'No file part in the request'})
		resp.status_code = 400
		return resp
	file = request.files['file']
	if file.filename == '':
		resp = jsonify({'message' : 'No file selected for uploading'})
		resp.status_code = 400
		return resp
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
		resp = jsonify({'message' : 'File successfully uploaded'})
		resp.status_code = 201
		return resp
	else:
		resp = jsonify({'message' : 'Allowed file type is .csv'})
		resp.status_code = 400
		return resp

@app.route('/search', methods=['GET'])
def search():
    try :
        args = request.args
        data = args.get('texttosearch')
        reply = tf.searchnlp(str(data))
        return jsonify({'Status Code ': 200, 'Text to Search': data, 'Request Id' : reply})
    except Exception as e:
        return jsonify({'Status Code ': 400,'Error': e})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
