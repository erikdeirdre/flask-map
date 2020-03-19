from os import environ
from os.path import (join, exists)
from flask import (Flask, request, jsonify)
from flask_googlemaps import (GoogleMaps, Map)
from flask_cors import CORS
from werkzeug.utils import secure_filename

from googlemaps import Client
import pandas

app = Flask(__name__, template_folder="templates")
app.config.from_object(environ.get('CONFIG_SETTINGS',
                                   "config.DevelopmentConfig"))
CORS(app)

file_name = 'addresses.xlsx'
GoogleMaps(app, key=app.config['GOOGLE_API_KEY'])
gmaps = Client(key=app.config['GOOGLE_API_KEY'])


def get_map_points(file_name):
    delivery_points = []

    if not exists(join(app.config['UPLOAD_FOLDER'], file_name)):
        return delivery_points

    addr_file = pandas.read_excel(file_name)

    for addr_index in addr_file.index:
        geocode_result = gmaps.geocode('{}, {}, {}'.format(
            addr_file['Address'][addr_index],
            addr_file['City'][addr_index],
            addr_file['State'][addr_index]))

        for entry in geocode_result:
            delivery_points.append({
                'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
                'lat': entry['geometry']['location']['lat'],
                'lng': entry['geometry']['location']['lng'],
                'address': addr_file['Address'][addr_index],
                'title': '{} {}'.format(
                    addr_file['First Name'][addr_index],
                    addr_file['Last Name'][addr_index])
            })

    return delivery_points


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in \
           app.config['ALLOWED_EXTENSIONS']


@app.route("/upload", methods=['GET', 'POST'])
def upload_file():
    global file_name
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            resp = jsonify({'message': 'No file part in the request'})
            resp.status_code = 400
            return resp
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            resp = jsonify({'message': 'No file selected for uploading'})
            resp.status_code = 400
            return resp
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(join(app.config['UPLOAD_FOLDER'], filename))
            file_name = filename
            resp = jsonify({'message': 'File successfully uploaded'})
            resp.status_code = 201
            return resp

        resp = jsonify({'message': 'Allowed file types are txt, pdf, png, jpg, jpeg, gif'})
        resp.status_code = 400
        return resp


@app.route("/map")
def map_view():
    return jsonify(get_map_points(join(app.config['UPLOAD_FOLDER'],
                                       file_name)))


if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])
