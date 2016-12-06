from __future__ import print_function
from PIL import Image

import io
import uuid

class ImageResize:
    def resize(self, stream, crop):
        print('Cropping direction:', crop)

        image = Image.open(io.BytesIO(stream))
        print('Image Stats:', image.format, image.size, image.mode)

        # Calculate image region to crop
        pointX = 0
        pointY = 0
        width, height = image.size
        region = (pointX, pointY, width, height)

        if crop.lower() == 'left':
            region = (pointX, pointY, int(width / 2), height)
        elif crop.lower() == 'right':
            region = (int(width / 2), pointY, width, height)

        # Crop the image with the calculated region
        with image.crop(region) as newImage:
            path = 'csn-' + str(uuid.uuid4()) + '.' + str(image.format)
            newImage.save(path)
            return path
