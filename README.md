# Use virtualenv to isolate pip installation
virtualenv --system-site-packages ~/tensorflow

source ~/tensorflow/bin/activate  

#Install dependency
pip install Pillow

pip install requests

pip install flask_restful

pip install cherrypy

#Run it
python server.py

To run in the background:

python server.py &
