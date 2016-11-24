from __future__ import print_function
from PIL import Image
from StringIO import StringIO

import uuid

class ImageResize:
    def resize(self, stream, crop):
        print('Cropping direction:', crop)

        image = Image.open(StringIO(stream))
        print('Image Stats:', image.format, image.size, image.mode)

        # Calculate image region to crop
        pointX = 0
        pointY = 0
        width, height = image.size
        region = (pointX, pointY, width, height)

        if crop == 'left':
            region = (pointX, pointY, int(width / 2), height)
        elif crop == 'right':
            region = (int(width / 2), pointY, width, height)

        # Crop the image with the calculated region
        with image.crop(region) as newImage:
            path = 'csn-' + str(uuid.uuid4()) + '.' + str(image.format)
            newImage.save(path)
            return path
