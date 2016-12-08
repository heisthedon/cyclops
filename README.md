# Use virtualenv to isolate pip installation
virtualenv --system-site-packages ~/tensorflow

source ~/tensorflow/bin/activate  

#Install dependencies
pip install -r requirements.txt

#Run it
python server.py

To run in the background:

python server.py &

# Run using Docker
sudo docker build --no-cache -t docker-cyclops .
sudo docker run -p 80:80 docker-cyclops
