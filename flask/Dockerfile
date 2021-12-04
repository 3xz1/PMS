# Use python 3.8 container image
FROM python:3.8

# Maintainer
MAINTAINER Alexander Eger <aeger1@stud.hs-offenburg.de>

# Working directroy
WORKDIR /flask

# Copy current directory to /app inside the container
ADD . /flask

# install requirements
RUN pip install -r requirements.txt
# run following commands
RUN chmod 777 /flask/scripts/commands.sh
CMD ["/flask/scripts/commands.sh"]
