import requests
import time
import json
import os

from flask_restful import Resource, Api, reqparse
from apps import app
from apps.image_resize import ImageResize
from apps.classification import Tensorflow

api = Api(app)

class Classify(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()

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
            default = "none",
            help = 'right | left | none',
            location = 'json')

        super(Classify, self).__init__()

    def post(self):
        postStart = time.time()

        args = self.reqparse.parse_args()

        start = time.time()
        response = requests.get(args.imageUrl, stream=True)
        downloadTimeElapsed = (time.time() - start)

        start = time.time()
        imgResize = ImageResize()
        imgOutputPath = imgResize.resize(response.content, args.imageCrop.lower())
        resizeTimeElapsed = (time.time() - start)

        start = time.time()

        classifyTimeElapsed = (time.time() - start)
        tf = Tensorflow()
        output = tf.execute(args.graph, imgOutputPath)
        os.remove(imgOutputPath)

        postEnd = time.time()

        return {
            'downloadImageSize': len(response.content),
            'downloadTimeElapsedMs': downloadTimeElapsed * 1000,
            'resizeTimeElapsedMs': resizeTimeElapsed * 1000,
            'resizeImagePath': imgOutputPath,
            'classifyOutput': output,
            'classifyCmd': cmd,
            'classifyTimeElapsedMs': classifyTimeElapsed * 1000,
            'totalTimeElapsedMs': (postEnd - postStart)
        }

api.add_resource(Classify, '/classify', endpoint = 'classify')
