## FROM python:3.9
## python:3.10-alpine
#FROM python:3.10-buster
##FROM python:3.10-bullseye
#
#
#WORKDIR /app
#
#COPY ./requirements.txt /app/requirements.txt
#
## RUN echo $PATH
## RUN echo "export PATH=$PATH:/usr/local/bin/docker" >> ~/.bashrc
## RUN cat ~/.bashrc
## RUN echo $PATH
#
#
#
#RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
#
#COPY . /app/
#
#CMD [ "uvicorn", "app.main:app", "--reload", "--workers", "1", "--host", "0.0.0.0", "--port", "80" ]
#
#COPY ./ /app/




###################################
FROM ubuntu:latest

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

# Install system dependencies
RUN apt-get update && apt-get install -y \
    python3.10 \
    python3.10-dev \
    python3-pip \
    libsm6 \
    libxext6 \
    libxrender-dev \
    libglib2.0-0 \
    libgl1-mesa-glx \
    libglib2.0-0 \
    libsm6 \
    libxext6 \
    libxrender-dev

##RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt
# Install OpenCV
RUN pip3 install opencv-python-headless

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app/

CMD [ "uvicorn", "app.main:app", "--reload", "--workers", "1", "--host", "0.0.0.0", "--port", "80" ]

COPY ./ /app/


