from flask import Flask, request,jsonify,render_template
import os
from flask_cors import CORS,cross_origin
from utils.utils import decodeImage
from predict import maskdetection
import shutil

os.putenv('LANG', 'en_US.UTF-8')
os.putenv('LC_ALL', 'en_US.UTF-8')

app = Flask(__name__)
CORS(app)

class ClientApp:
    def __init__(self):
        self.filename = "inputImage.jpg"
        self.classifier = maskdetection(self.filename)

@app.route("/", methods=["GET"])
@cross_origin()
def home():
    return render_template('index.html')

@app.route("/predict",methods=['POST'])
@cross_origin()
def predictRoute():
    try:
        image = request.json['image']
        decodeImage(image,ClientApp().filename)
        result = ClientApp().classifier.predictionmask()
        return jsonify(result)

        
    except ValueError:
        return jsonify({"error":"Error Occurred! %s"})
    except KeyError:
        return jsonify({"error":"Error Occurred! %s"})
    except Exception as e:
        return jsonify({"error":"Error Occurred! %s"})


if __name__ == "__main__":
    app.run(debug=True)