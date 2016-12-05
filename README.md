# Use virtualenv to isolate pip installation
virtualenv --system-site-packages ~/tensorflow

source ~/tensorflow/bin/activate  

pip install Pillow==2.6.1

pip install requests

pip install flask_restful

python run.py
