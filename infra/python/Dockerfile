FROM selenium/standalone-chrome

RUN sudo apt update \
  && sudo apt -y install python3-pip

RUN pip install selenium numpy opencv-python python-dotenv

WORKDIR /usr/src
