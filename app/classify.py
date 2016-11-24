import requests
import time

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
        imgResize.resize(response.content, args.imageCrop.lower())
        resizeTimeElapsed = (time.clock() - start)

        return {
            'downloadImageSize': len(response.content),
            'downloadTimeElapsedMs': downloadTimeElapsed * 1000,
            'resizeTimeElapsedMs': resizeTimeElapsed * 1000
        }

api.add_resource(Classify, '/classify', endpoint = 'classify')
