############################################################
# Dockerfile to build Python WSGI Application Containers
# Based on Ubuntu
############################################################

# Set the base image to Ubuntu
FROM cyclops:python-setup

# File Author / Maintainer
MAINTAINER Hery

# Update the sources list
RUN apt-get update

# Get pip to download and install requirements:
#RUN pip install -r ~/cyclops/requirement.txt

# Expose ports
EXPOSE 80

# Set the default directory where CMD will execute
WORKDIR /cyclops

RUN git pull origin master

RUN pip install -r requirement.txt

RUN chmod 755 -R .

# Set the default command to execute
# when creating a new container
# i.e. using CherryPy to serve the application
CMD python server.py
