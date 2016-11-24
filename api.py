from flask import Flask, request
from flask_restful import Resource, Api, reqparse

app = Flask(__name__)
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

        super(Classify, self).__init__()

    def post(self):
        args = self.reqparse.parse_args()
        return {'hello': args.imageUrl }

api.add_resource(Classify, '/classify', endpoint = 'classify')

if __name__ == '__main__':
    app.run(debug=True)
