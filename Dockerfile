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

RUN pip3 install opencv-python-headless

RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

COPY . /app/

CMD [ "uvicorn", "app.main:app", "--reload", "--workers", "1", "--host", "0.0.0.0", "--port", "80" ]

COPY ./ /app/


