import requests
import time
import subprocess

from flask_restful import Resource, Api, reqparse
from app import app
from image_resize import ImageResize

api = Api(app)

class Classify(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('v', type = int, location = 'args')

        self.reqparse.add_argument('graph',
            type = str,
            required = True,
            help = '',
            location = 'json')

        self.reqparse.add_argument('imageUrl',
            type = str,
            required = True,
            help = 'Image Url to download',
            location = 'json')

        self.reqparse.add_argument('imageCrop',
            type = str,
            required = False,
            default = "",
            help = 'Right | Left',
            location = 'json')

        super(Classify, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()

        start = time.clock()
        response = requests.get(args.imageUrl, stream=True)
        downloadTimeElapsed = (time.clock() - start)

        start = time.clock()
        imgResize = ImageResize()
        imgOutput = imgResize.resize(response.content, args.imageCrop.lower())
        resizeTimeElapsed = (time.clock() - start)

        cmd = "tensorflow/label_image/label_image --graph=%s.pb --labels=%s.txt --output_layer=final_result --image=%s" %(args.graph, args.graph, imgOutput)
        print cmd
        return_code = subprocess.call(cmd, shell=True)

        return {
            'downloadImageSize': len(response.content),
            'downloadTimeElapsedMs': downloadTimeElapsed * 1000,
            'resizeTimeElapsedMs': resizeTimeElapsed * 1000,
            'resizeImagePath': imgOutput,
            'classifyReturnCode': return_code
        }

api.add_resource(Classify, '/classify', endpoint = 'classify')
