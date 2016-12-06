import requests
import time
import subprocess
import json
import os

from flask_restful import Resource, Api, reqparse
from app import app
from PIL import Image

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
        img = Image.open(StringIO(response.content))
        imgOutput = img.crop(args.imageCrop.lower())
        resizeTimeElapsed = (time.time() - start)

        start = time.time()
        cmd = ["tensorflow/label_image/label_image"
                , "--graph=tensorflow/graph/%s.pb" %(args.graph)
                , "--labels=tensorflow/graph/%s.txt" %(args.graph)
                , "--output_layer=final_result"
                , "--image=%s" %(imgOutput)]
        proc = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        (output, err) = proc.communicate()
        classifyTimeElapsed = (time.time() - start)

        os.remove(imgOutput)

        postEnd = time.time()

        return {
            'downloadImageSize': len(response.content),
            'downloadTimeElapsedMs': downloadTimeElapsed * 1000,
            'resizeTimeElapsedMs': resizeTimeElapsed * 1000,
            'resizeImagePath': imgOutput,
            'classifyOutput': json.loads(output),
            'classifyCmd': cmd,
            'classifyTimeElapsedMs': classifyTimeElapsed * 1000,
            'totalTimeElapsedMs': (postEnd - postStart)
        }

api.add_resource(Classify, '/classify', endpoint = 'classify')
