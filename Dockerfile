# Set the base image to Ubuntu
FROM ubuntu

# File Author / Maintainer
MAINTAINER Stephen Nguyen (@Stephenitis)

# Add the application resources URL
RUN echo "deb http://archive.ubuntu.com/ubuntu/ $(lsb_release -sc) main universe" >> /etc/apt/sources.list

# Update the sources list
RUN apt-get update

# Install basic applications
RUN apt-get install -y tar git curl nano wget dialog net-tools build-essential

# Install Python and Basic Python Tools
RUN apt-get install -y python python-dev python-distribute python-pip
RUN pip install TwitterAPI

RUN apt-get build-dep psycopg2 -y
RUN  pip install psycopg2
RUN apt-get install python-dev libffi-dev libssl-dev -y
RUN pip install pyopenssl ndg-httpsclient pyasn1
RUN pip install --ignore-installed 'requests[security]'
RUN pip install --upgrade requests
# Copy the application folder inside the container

ADD generate-workload.py .

# Set the default directory where CMD will execute
WORKDIR .

CMD [ "python", "./generate-workload.py" ]
